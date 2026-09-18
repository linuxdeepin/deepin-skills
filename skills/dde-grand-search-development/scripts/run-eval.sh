#!/bin/sh

set -eu

usage() {
    cat <<'EOF'
Usage: scripts/run-eval.sh --eval FILE [options] -- AGENT_COMMAND [ARG...]

Run one Markdown output-quality eval with and without this skill.
AGENT_COMMAND must read the prompt from standard input and honor SKILL_HOME.

Options:
  --eval FILE       Eval Markdown file containing "## 任务" and "## 验证要点".
  --runs N          Runs per variant (default: 3).
  --output DIR      Result directory (default: ./eval-workspace/<skill>/<timestamp>).
  --fixture DIR     Copy fixture contents into each isolated run workspace.
  -h, --help        Show this help.
EOF
}

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
skill_root=$(dirname "$script_dir")
skill=$(basename "$skill_root")
eval_file=
runs=3
output_dir=
fixture_dir=

while [ "$#" -gt 0 ]; do
    case "$1" in
        --eval)
            [ "$#" -ge 2 ] || { usage >&2; exit 2; }
            eval_file=$2
            shift 2
            ;;
        --runs)
            [ "$#" -ge 2 ] || { usage >&2; exit 2; }
            runs=$2
            shift 2
            ;;
        --output)
            [ "$#" -ge 2 ] || { usage >&2; exit 2; }
            output_dir=$2
            shift 2
            ;;
        --fixture)
            [ "$#" -ge 2 ] || { usage >&2; exit 2; }
            fixture_dir=$2
            shift 2
            ;;
        --)
            shift
            break
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            usage >&2
            exit 2
            ;;
    esac
done

[ -n "$eval_file" ] || { echo "--eval is required" >&2; exit 2; }
[ -f "$eval_file" ] || { echo "Eval file not found: $eval_file" >&2; exit 2; }
[ "$#" -gt 0 ] || { echo "AGENT_COMMAND is required after --" >&2; exit 2; }
case "$runs" in *[!0-9]*|'') echo "--runs must be a positive integer" >&2; exit 2;; esac
[ "$runs" -gt 0 ] || { echo "--runs must be a positive integer" >&2; exit 2; }
if [ -n "$fixture_dir" ] && [ ! -d "$fixture_dir" ]; then
    echo "Fixture directory not found: $fixture_dir" >&2
    exit 2
fi

if [ -z "$output_dir" ]; then
    output_dir="$PWD/eval-workspace/$skill/$(date +%Y%m%d-%H%M%S)"
fi
mkdir -p "$output_dir"
output_dir=$(CDPATH= cd -- "$output_dir" && pwd)

temp_dir=$(mktemp -d "${TMPDIR:-/tmp}/skill-eval.XXXXXX")
trap 'rm -rf "$temp_dir"' 0 HUP INT TERM
task_file="$temp_dir/task.md"
checks_file="$temp_dir/checks.md"

awk '/^## 任务[[:space:]]*$/{capture=1; next} /^## /{if (capture) exit} capture{print}' "$eval_file" > "$task_file"
awk '/^## 验证要点[[:space:]]*$/{capture=1; next} /^## /{if (capture) exit} capture{print}' "$eval_file" > "$checks_file"
[ -s "$task_file" ] || { echo "No task found under ## 任务 in $eval_file" >&2; exit 2; }
[ -s "$checks_file" ] || { echo "No checks found under ## 验证要点 in $eval_file" >&2; exit 2; }

printf 'variant\trun\texit_code\tduration_seconds\n' > "$output_dir/summary.tsv"

for variant in with_skill baseline; do
    run=1
    while [ "$run" -le "$runs" ]; do
        run_dir="$output_dir/$variant/run-$run"
        workspace="$run_dir/workspace"
        profile="$temp_dir/$variant-$run/profile"
        mkdir -p "$workspace" "$profile/skills"
        if [ -n "$fixture_dir" ]; then
            cp -R "$fixture_dir"/. "$workspace"/
        fi
        if [ "$variant" = with_skill ]; then
            installed_skill="$profile/skills/$skill"
            mkdir -p "$installed_skill"
            cp "$skill_root/SKILL.md" "$installed_skill/"
            for resource_dir in agents references scripts assets; do
                if [ -d "$skill_root/$resource_dir" ]; then
                    cp -R "$skill_root/$resource_dir" "$installed_skill/"
                fi
            done
            {
                printf 'Use $%s to complete this task.\n\n' "$skill"
                cat "$task_file"
            } > "$run_dir/prompt.md"
        else
            cp "$task_file" "$run_dir/prompt.md"
        fi
        cp "$checks_file" "$run_dir/grading.md"

        started=$(date +%s)
        set +e
        (cd "$workspace" && SKILL_HOME="$profile" "$@" < "$run_dir/prompt.md") \
            > "$run_dir/response.md" 2> "$run_dir/stderr.log"
        exit_code=$?
        set -e
        finished=$(date +%s)
        duration=$((finished - started))

        cat > "$run_dir/timing.json" <<EOF
{"exit_code":$exit_code,"duration_seconds":$duration,"total_tokens":null}
EOF
        printf '%s\t%s\t%s\t%s\n' "$variant" "$run" "$exit_code" "$duration" >> "$output_dir/summary.tsv"
        run=$((run + 1))
    done
done

printf 'Results written to %s\n' "$output_dir"
printf 'Grade each run in grading.md with evidence, then compare pass rate, time, and output quality.\n'
