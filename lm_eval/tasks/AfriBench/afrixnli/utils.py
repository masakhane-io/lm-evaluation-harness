import argparse

import yaml


class FunctionTag:
    def __init__(self, value):
        self.value = value


def prompt_func(mode, lang):
    prompt_map = {
        "prompt_3": f"Given the following premise and hypothesis in {lang}, identify if the premise entails, contradicts, "
                    f"or is neutral towards the hypothesis. Please respond with exact 'entailment', 'contradiction', or 'neutral'. \n\n"
                    "Premise: {{premise}} \nHypothesis: {{hypothesis}}",
        "prompt_4": f"You are an expert in Natural Language Inference (NLI) specializing in the {lang} language.\n"
                    f"Analyze the premise and hypothesis given in {lang}, and determine the relationship between them.\n "
                    f"Respond with one of the following options: 'entailment', 'contradiction', or 'neutral'. \n\n"
                    "Premise: {{premise}} \nHypothesis: {{hypothesis}}",
        "prompt_5": "Based on the given statement, is the following claim 'true', 'false', or 'inconclusive'. \n"
                    "Statement: {{premise}} \nClaim: {{hypothesis}}"
    }
    return prompt_map[mode]


def gen_lang_yamls(output_dir: str, overwrite: bool, mode: str) -> None:
    """
    Generate a yaml file for each language.

    :param output_dir: The directory to output the files to.
    :param overwrite: Whether to overwrite files if they already exist.
    """
    err = []
    languages = {
        "eng": "English",
        "amh": "Amharic",
        "ibo": "Igbo",
        "fra": "French",
        "sna": "chiShona",
        "wol": "Wolof",
        "ewe": "Ewe",
        "lin": "Lingala",
        "lug": "Luganda",
        "xho": "isiXhosa",
        "kin": "Kinyarwanda",
        "twi": "Twi",
        "zul": "Zulu",
        "orm": "Oromo",
        "yor": "Yoruba",
        "hau": "Hausa",
        "sot": "Sesotho",
        "swa": "Swahili",
    }

    for lang in languages.keys():
        try:
            file_name = f"afrixnli_{lang}.yaml"
            task_name = f"afrixnli_{lang}_{mode}"
            yaml_template = f"afrixnli_yaml"
            if int(mode.split("_")[-1]) > 2:
                yaml_details = {
                        "include": yaml_template,
                        "task": task_name,
                        "dataset_name": lang,
                        "doc_to_text": prompt_func(mode, languages[lang])
                    }
            else:
                yaml_details = {
                        "include": yaml_template,
                        "task": task_name,
                        "dataset_name": lang,
                    }
            with open(
                    f"{output_dir}/{mode}/{file_name}",
                    "w" if overwrite else "x",
                    encoding="utf8",
            ) as f:
                f.write("# Generated by utils.py\n")
                yaml.dump(
                    yaml_details,
                    f,
                    allow_unicode=True,
                )
        except FileExistsError:
            err.append(file_name)

    if len(err) > 0:
        raise FileExistsError(
            "Files were not created because they already exist (use --overwrite flag):"
            f" {', '.join(err)}"
        )


def main() -> None:
    """Parse CLI args and generate language-specific yaml files."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--overwrite",
        default=True,
        action="store_true",
        help="Overwrite files if they already exist",
    )
    parser.add_argument(
        "--output-dir",
        default="./",
        help="Directory to write yaml files to",
    )
    parser.add_argument(
        "--mode",
        default="prompt_4",
        choices=["prompt_1", "prompt_2", "prompt_3", "prompt_4", "prompt_5"],
        help="Prompt number",
    )
    args = parser.parse_args()

    gen_lang_yamls(output_dir=args.output_dir, overwrite=args.overwrite, mode=args.mode)


if __name__ == "__main__":
    main()
