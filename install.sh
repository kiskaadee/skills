#!/usr/bin/env bash
# install.sh — Install and link/copy skills to agent configuration directories
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${TARGET:-$HOME/.gemini/config/skills}"
PROFILE_TARGET="${PROFILE_TARGET:-$HOME/.gemini/config/AGENTS.md}"
AGENTS_DIR_TARGET="${AGENTS_DIR_TARGET:-$HOME/.gemini/config/agents}"
MODE="link"
CHECK_ONLY=0

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)
      MODE="$2"
      shift 2
      ;;
    --target)
      TARGET_DIR="$2"
      shift 2
      ;;
    check|--check)
      CHECK_ONLY=1
      shift
      ;;
    *)
      echo "Unknown option: $1" >&2
      echo "Usage: ./install.sh [--mode link|copy] [--target DIR] [check]" >&2
      exit 1
      ;;
  esac
done

# Active skills to install
ACTIVE_PORTABLE_SKILLS=(build-skill diagnose document git-commit journal-builder practice)
ACTIVE_EXTENSION_SKILLS=(draft-curation commit-logger)

# Legacy / deprecated skills to clean up or back up if found in target
OBSOLETE_SKILLS=(engineering-tutor engineering-investigation skill-builder documentation-router inbox-curation)

echo "=== Target: $TARGET_DIR (mode: $MODE) ==="

if [[ "$CHECK_ONLY" -eq 1 ]]; then
  echo "Checking installation state..."
  missing=0
  for s in "${ACTIVE_PORTABLE_SKILLS[@]}"; do
    if [[ ! -e "$TARGET_DIR/$s" ]]; then
      echo "  [MISSING] $s"
      missing=$((missing + 1))
    fi
  done
  for s in "${ACTIVE_EXTENSION_SKILLS[@]}"; do
    if [[ ! -e "$TARGET_DIR/$s" ]]; then
      echo "  [MISSING] $s (extension)"
      missing=$((missing + 1))
    fi
  done
  for obs in "${OBSOLETE_SKILLS[@]}"; do
    if [[ -e "$TARGET_DIR/$obs" || -L "$TARGET_DIR/$obs" ]]; then
      echo "  [OBSOLETE PRESENT] $obs"
    fi
  done
  if [[ -d "$SCRIPT_DIR/profile/agents" ]]; then
    for a in "$SCRIPT_DIR/profile/agents"/*.md; do
      [[ -e "$a" ]] || continue
      aname="$(basename "$a")"
      if [[ ! -e "$AGENTS_DIR_TARGET/$aname" ]]; then
        echo "  [MISSING] agent: $aname"
        missing=$((missing + 1))
      fi
    done
  fi
  if [[ "$missing" -eq 0 ]]; then
    echo "All active skills are present."
  fi
  exit 0
fi

# Prepare backup directory timestamp if needed
BACKUP_DIR="${TARGET_DIR}.backup-$(date +%Y%m%d%H%M%S)"
backed_up=0

backup_if_exists() {
  local path="$1"
  if [[ -e "$path" || -L "$path" ]]; then
    if [[ "$backed_up" -eq 0 ]]; then
      mkdir -p "$BACKUP_DIR"
      backed_up=1
    fi
    mv "$path" "$BACKUP_DIR/"
    echo "  [BACKUP] $(basename "$path") -> $BACKUP_DIR/"
  fi
}

mkdir -p "$TARGET_DIR"

# Clean up obsolete skills
for obs in "${OBSOLETE_SKILLS[@]}"; do
  if [[ -e "$TARGET_DIR/$obs" || -L "$TARGET_DIR/$obs" ]]; then
    backup_if_exists "$TARGET_DIR/$obs"
  fi
done

# Install portable skills
for s in "${ACTIVE_PORTABLE_SKILLS[@]}"; do
  src="$SCRIPT_DIR/skills/$s"
  dest="$TARGET_DIR/$s"

  # Backup existing if it's not a symlink pointing to the right source
  if [[ -L "$dest" ]]; then
    target_link="$(readlink "$dest")"
    if [[ "$target_link" != "$src" ]]; then
      rm -f "$dest"
    fi
  elif [[ -d "$dest" ]]; then
    backup_if_exists "$dest"
  fi

  if [[ "$MODE" == "link" ]]; then
    ln -sfn "$src" "$dest"
    echo "  [LINKED] $s -> $dest"
  elif [[ "$MODE" == "copy" ]]; then
    mkdir -p "$dest"
    rsync -a --delete "$src/" "$dest/"
    echo "$SCRIPT_DIR@$(git -C "$SCRIPT_DIR" rev-parse HEAD 2>/dev/null || echo unknown)" > "$dest/.managed-by-skills-repo"
    echo "  [COPIED] $s -> $dest"
  fi
done

# Install extension skills
for s in "${ACTIVE_EXTENSION_SKILLS[@]}"; do
  src="$SCRIPT_DIR/extensions/$s"
  dest="$TARGET_DIR/$s"

  if [[ -L "$dest" ]]; then
    target_link="$(readlink "$dest")"
    if [[ "$target_link" != "$src" ]]; then
      rm -f "$dest"
    fi
  elif [[ -d "$dest" ]]; then
    backup_if_exists "$dest"
  fi

  if [[ "$MODE" == "link" ]]; then
    ln -sfn "$src" "$dest"
    echo "  [LINKED] $s (extension) -> $dest"
  elif [[ "$MODE" == "copy" ]]; then
    mkdir -p "$dest"
    rsync -a --delete "$src/" "$dest/"
    echo "$SCRIPT_DIR@$(git -C "$SCRIPT_DIR" rev-parse HEAD 2>/dev/null || echo unknown)" > "$dest/.managed-by-skills-repo"
    echo "  [COPIED] $s (extension) -> $dest"
  fi
done

# Install global AGENTS.md profile if parent directory exists
if [[ -d "$(dirname "$PROFILE_TARGET")" ]]; then
  profile_src="$SCRIPT_DIR/profile/AGENTS.md"
  if [[ -L "$PROFILE_TARGET" ]]; then
    target_link="$(readlink "$PROFILE_TARGET")"
    if [[ "$target_link" != "$profile_src" ]]; then
      rm -f "$PROFILE_TARGET"
    fi
  elif [[ -f "$PROFILE_TARGET" ]]; then
    profile_backup="${PROFILE_TARGET}.backup-$(date +%Y%m%d%H%M%S)"
    cp "$PROFILE_TARGET" "$profile_backup"
    echo "  [BACKUP] $PROFILE_TARGET -> $profile_backup"
  fi

  if [[ "$MODE" == "link" ]]; then
    ln -sfn "$profile_src" "$PROFILE_TARGET"
    echo "  [LINKED] AGENTS.md -> $PROFILE_TARGET"
  elif [[ "$MODE" == "copy" ]]; then
    cp "$profile_src" "$PROFILE_TARGET"
    echo "  [COPIED] AGENTS.md -> $PROFILE_TARGET"
  fi
fi

# Install agent personas
if [[ -d "$SCRIPT_DIR/profile/agents" ]]; then
  mkdir -p "$AGENTS_DIR_TARGET"
  for a in "$SCRIPT_DIR/profile/agents"/*.md; do
    [[ -e "$a" ]] || continue
    aname="$(basename "$a")"
    adest="$AGENTS_DIR_TARGET/$aname"
    if [[ -L "$adest" ]]; then
      target_link="$(readlink "$adest")"
      if [[ "$target_link" != "$a" ]]; then
        rm -f "$adest"
      fi
    elif [[ -f "$adest" ]]; then
      backup_if_exists "$adest"
    fi

    if [[ "$MODE" == "link" ]]; then
      ln -sfn "$a" "$adest"
      echo "  [LINKED] agent: $aname -> $adest"
    elif [[ "$MODE" == "copy" ]]; then
      cp "$a" "$adest"
      echo "  [COPIED] agent: $aname -> $adest"
    fi
  done
fi

if [[ "$backed_up" -eq 1 ]]; then
  echo "Backups stored in: $BACKUP_DIR"
fi
echo "Installation complete."
