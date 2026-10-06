#!/usr/bin/env bash
# AI 短剧制作学院 · 一键装载脚本（install.sh）
#
# 用途：把 20-craft/*/ 里每个带 SKILL.md 的技能以符号链接装进运行时的技能目录；
#       记录学院根目录到 $ACADEMY_HOME/.academy_home；打印 Top-12 记忆行供粘贴进长期记忆。
# 特性：幂等（重复运行结果相同）、无网络、只读学院仓库（唯一写入：$ACADEMY_HOME/.academy_home 与技能目录里的链接）。
# 溯源：委托方实证 E3-3（技能装配期一次性扫描，装/改后必须重启运行时）、E3-1（路径用纯英文）。
# 完整协议：90-curriculum/load-protocol.md
#
# 用法：
#   bash 90-curriculum/install/install.sh                                  # 装到 ~/.claude/skills
#   bash 90-curriculum/install/install.sh --target-skills-dir DIR          # 装到别的技能目录（项目级 .claude/skills、Codex 技能目录等）
#   bash 90-curriculum/install/install.sh --dry-run                        # 只打印将做什么，不改任何文件
# 退出码：0 成功 / 1 有冲突被跳过（目标位置已有同名真实目录或文件） / 2 用法或环境错误
set -euo pipefail

TARGET_SKILLS_DIR="${HOME}/.claude/skills"
DRY_RUN=0

usage() {
  sed -n '2,15p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --target-skills-dir)
      if [ "$#" -lt 2 ] || [ -z "${2:-}" ]; then echo "错误：--target-skills-dir 需要一个目录参数" >&2; exit 2; fi
      TARGET_SKILLS_DIR="$2"; shift 2 ;;
    --target-skills-dir=*)
      TARGET_SKILLS_DIR="${1#*=}"
      if [ -z "$TARGET_SKILLS_DIR" ]; then echo "错误：--target-skills-dir 不能为空" >&2; exit 2; fi
      shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "错误：未知参数 $1（可用：--target-skills-dir DIR、--dry-run、-h）" >&2; exit 2 ;;
  esac
done

# 展开前导 ~（用户可能传 "~/.codex/skills"）
case "$TARGET_SKILLS_DIR" in
  "~") TARGET_SKILLS_DIR="$HOME" ;;
  "~/"*) TARGET_SKILLS_DIR="$HOME/${TARGET_SKILLS_DIR#\~/}" ;;
esac

# 从脚本位置解析学院根目录（脚本在 <ACADEMY_HOME>/90-curriculum/install/install.sh）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ACADEMY_HOME="$(cd "$SCRIPT_DIR/../.." && pwd)"

if [ ! -d "$ACADEMY_HOME/20-craft" ] || [ ! -f "$ACADEMY_HOME/40-memory/core-memory.md" ]; then
  echo "错误：$ACADEMY_HOME 不像学院根目录（缺 20-craft/ 或 40-memory/core-memory.md）。请从完整克隆里运行本脚本。" >&2
  exit 2
fi

if printf '%s' "$ACADEMY_HOME" | LC_ALL=C grep -q '[^[:print:]]' || [ "${ACADEMY_HOME#* }" != "$ACADEMY_HOME" ]; then
  echo "警告：学院根目录路径含非 ASCII 字符或空格：$ACADEMY_HOME" >&2
  echo "      委托方实证 E3-1：中文路径会在 cmd 裸跑时吞输出。建议克隆到纯英文、无空格路径后重装。" >&2
fi

say() { printf '%s\n' "$*"; }
run() { if [ "$DRY_RUN" -eq 1 ]; then say "[dry-run] $*"; else "$@"; fi; }

say "== 学院根目录 ACADEMY_HOME = $ACADEMY_HOME"
say "== 目标技能目录            = $TARGET_SKILLS_DIR"
[ "$DRY_RUN" -eq 1 ] && say "== 模式：dry-run（不改任何文件）"

# 1) 技能：20-craft/<name>/（含 SKILL.md）→ 符号链接
say ""
say "== 1/4 装载技能"
run mkdir -p "$TARGET_SKILLS_DIR"

n_new=0; n_upd=0; n_same=0; n_conflict=0; n_total=0
for d in "$ACADEMY_HOME"/20-craft/*/; do
  [ -f "${d}SKILL.md" ] || continue
  name="$(basename "$d")"
  src="${d%/}"
  dst="$TARGET_SKILLS_DIR/$name"
  n_total=$((n_total + 1))
  if [ -L "$dst" ]; then
    cur="$(readlink "$dst")"
    if [ "$cur" = "$src" ]; then
      say "  = $name（已链接，未变）"; n_same=$((n_same + 1))
    else
      say "  ~ $name（链接指向 $cur → 更新为 $src）"
      run ln -sfn "$src" "$dst"; n_upd=$((n_upd + 1))
    fi
  elif [ -e "$dst" ]; then
    say "  ! $name（$dst 已存在且不是符号链接，已跳过；若是旧的拷贝请手动移走后重跑）" >&2
    n_conflict=$((n_conflict + 1))
  else
    say "  + $name"
    run ln -s "$src" "$dst"; n_new=$((n_new + 1))
  fi
done
say "  小计：共 $n_total 个技能；新增 $n_new，更新 $n_upd，未变 $n_same，冲突跳过 $n_conflict"
if [ "$n_total" -eq 0 ]; then echo "错误：20-craft/ 下没有任何带 SKILL.md 的技能目录" >&2; exit 2; fi

# 2) 记录学院根目录
say ""
say "== 2/4 记录学院根目录"
HOME_FILE="$ACADEMY_HOME/.academy_home"
if [ -f "$HOME_FILE" ] && [ "$(cat "$HOME_FILE")" = "$ACADEMY_HOME" ]; then
  say "  = $HOME_FILE（已是 $ACADEMY_HOME）"
elif [ "$DRY_RUN" -eq 1 ]; then
  say "  [dry-run] 将写入 $HOME_FILE：$ACADEMY_HOME"
else
  printf '%s\n' "$ACADEMY_HOME" > "$HOME_FILE"
  say "  + 已写入 $HOME_FILE"
fi

# 3) 打印 Top-12 记忆（core-memory.md 第一个 ## 标题下的 MEM 行）
say ""
say "== 3/4 Top-12 记忆（逐字粘贴进运行时的长期记忆；Claude Code：~/.claude/CLAUDE.md 或项目 CLAUDE.md / 记忆库；Codex：AGENTS.md）"
say "-------- BEGIN MEMORY --------"
awk '
  /^## / { n++; next }
  n == 1 && /^- \[MEM-[0-9]+\]/ { print }
' "$ACADEMY_HOME/40-memory/core-memory.md"
say "- [MEM-ROOT][学院] 学院根目录 = $ACADEMY_HOME；技能里 60-casebook/... 等路径相对此根。（为什么：技能正文用根相对路径引用案例卡/清单/脚本，运行时不会替你解析）〔溯源：E3-3〕"
say "-------- END MEMORY --------"
n_mem="$(awk '/^## /{n++; next} n==1 && /^- \[MEM-[0-9]+\]/{c++} END{print c+0}' "$ACADEMY_HOME/40-memory/core-memory.md")"
say "  （共 $n_mem 条 Top-12 + 1 条根目录条目。Top-12 必须恰为 12 条；不是 12 请检查 core-memory.md。）"
say "  上面最后一条的 MEM-ROOT 是安装脚本生成的条目，用于让技能里的相对路径可解析；不属于 core-memory.md 的编号体系。"

# 4) 收尾
say ""
say "== 4/4 下一步"
say "  请重启运行时（委托方实证 E3-3：技能在装配期一次性扫描，不重启不生效）。"
say "  重启后：让 agent 读 90-curriculum/entry-prompt.md，并完成 90-curriculum/training-loop.md 的最低学分。"
say "  合规提醒：H3 排除地域与 Qwen-Image-2.1 研究许可见 00-orientation/evidence-reconciliation.md 第四部分，发布前由人类拍板。"

if [ "$n_conflict" -gt 0 ]; then
  echo "退出码 1：有 $n_conflict 个技能因目标位置已有同名真实目录/文件而被跳过。" >&2
  exit 1
fi
exit 0
