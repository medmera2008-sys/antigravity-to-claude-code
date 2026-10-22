# AGY Code Constitution

The tool injects code-constitution rules and swarm constraints into Google Antigravity.

## What it writes

| Component | Target Path | Description |
| :--- | :--- | :--- |
| **Rule** | `~/.gemini/antigravity-cli/rules/antigravity-to-claude-code.md` | Native system engine rule loaded on Antigravity sessions. |
| **Skill** | `~/.agents/skills/code-constitution/SKILL.md` | Global progressive manual discovered by Antigravity agents. |
| **Workspace Manifest** | `<project>/AGENTS.md` | Workspace instructions written inside the project directory via `inject.py`. |

The user home manifest `~/AGENTS.md` is never touched by default; it is modified only when the explicit `--with-home-agents` flag is provided.

## Installation

Clone the repository locally:

```bash
git clone https://github.com/medmera2008-sys/antigravity-to-claude-code.git
cd antigravity-to-claude-code
./install.sh
python3 inject.py --workspace /path/to/existing/project
```

Global installation of the native rule and skill is performed via `./install.sh` or `python3 inject.py --global`. Replacing the user home manifest requires adding `--with-home-agents`, which creates a timestamped backup (`AGENTS.md.bak.<UTC>`) before replacing `~/AGENTS.md`.

Both `./install.sh` and `inject.py` support `--dry-run` to inspect target paths and planned actions without writing any files.

## Uninstallation

To remove the globally injected rule and skill:

```bash
rm -f ~/.gemini/antigravity-cli/rules/antigravity-to-claude-code.md
rm -rf ~/.agents/skills/code-constitution
```

Deleting `AGENTS.md` in a workspace project or in the home directory is a manual decision, as those files may contain subsequent modifications. If `~/GEMINI.md` was created as a symlink by this installation, remove or restore it manually.

## Documentation Reference

The complete manual is documented in `skills/code-constitution/SKILL.md`, and the concise rule summary is maintained in `AGENTS.md`.

## Summaries

<details>
<summary><b>العربية (Arabic Summary)</b></summary>
<br>

1. **منع الحالة غير المهيّأة**: لا يُسند متغير داخل فرع شرطي أو معالج استثناء قبل تهيئته في النطاق الخارجي. كل إسناد داخل فرع يلزمه `else` أو رجوع مبكر.
2. **الحذف ثم الاستبدال ثم الإضافة**: إصلاح الخلل يبدأ بحذف المنطق الزائد، ثم التعديل في المكان. إضافة دالة أو تجريد تأتي بعد ذلك.
3. **منع الإخفاء والفشل الفوري**: التحقق على حدود النظام الخارجية. ابتلاع الاستثناء حول مكوّن داخلي واجب الوجود ممنوع.
4. **فحص السلوك المحذوف**: قبل حذف سطر، يُحدَّد الشرط الذي كان يحفظه. الحالة الجديدة تحفظه، أو يكون سقوطه مثبتاً.
5. **حوكمة الوكلاء**: الموجّه يحدّد المسارات والأسطر والفرضية. الوكيل الفرعي يعيد الخلاصة، ويعمل على شجرة عمل معزولة عند تعديل عدة ملفات.

</details>

<details>
<summary><b>한국어 (Korean Summary)</b></summary>
<br>

1. **비바운드 상태 배제**: 외부 스코프에서 기본값 초기화 없이 조건문이나 예외 블록 내에서 변수를 할당하는 행위를 금지하며, 모든 분기에는 `else` 또는 조기 반환이 필요합니다.
2. **삭제, 대체, 추가 순서**: 버그 수정은 중복 로직의 삭제 및 제자리 수정을 최우선으로 하며, 새로운 함수나 추상화 추가는 마지막에 고려합니다.
3. **은폐 금지 및 조기 실패**: 시스템 외부 경계에서만 방어적 검증을 수행하고, 필수 내부 구성 요소에 대한 예외 은폐를 금지하며 즉각 실패하도록 합니다.
4. **삭제된 동작 검증**: 코드를 삭제하기 전 해당 라인이 보호하던 기존 불변식을 식별하고 검증합니다.
5. **스웜 거버넌스**: 오케스트레이터가 경로와 라인, 가설을 직접 지정하며, 하위 에이전트는 결론만 전달하고 다중 파일 수정 시 격리된 작업 트리에서 실행합니다.

</details>

## Author & License

* **Author**: [@medismera](https://x.com/medismera)
* **License**: [MIT License](LICENSE)
