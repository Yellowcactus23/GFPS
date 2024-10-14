# python

# Date: 2024-10-13
# Author: Paul Fabian
# Modified:
# Description: This project helps track scores for the GFPS metric.

import os
import pandas as pd

from datetime import date

BASE_DIR = os.getcwd()


class GFPS:
    def __init__(self):

        # params
        self.BASE_DIR = BASE_DIR
        self.fast_test = False

        # dir check
        os.makedirs(os.path.join(BASE_DIR, "results"), exist_ok=True)

        # score and rank params
        self.score_params = self._load_score_params()
        self.rank_params = self._load_rank_params()
        self.eval_types = self.score_params.keys()

        self.prompt_new_entry = False
        self.prompt_update_eval = False

        # person entering the analyses
        if self.fast_test:
            self.users_name = "paul_fabian"
        else:
            self.users_name = self._get_name()

        self.user_dir = os.path.join(BASE_DIR, "results", self.users_name)

        welcome_message = f"""---------------------------\nWelcome to GFPS {self.users_name.title().replace("_", " ")}!\n---------------------------"""

        if not os.path.exists(self.user_dir):
            os.makedirs(self.user_dir)
        else:
            self.current_evals = self._get_current_evaluees()
            welcome_message = welcome_message.replace(" to ", " back to ")

        print(welcome_message)

    def main(self):

        # 1. New entries
        self.prompt_new_entry = self._check_another_reponse()
        while self.prompt_new_entry:
            self.new_entry()

        # 2. Update entries
        self.prompt_update_eval = self._check_update_eval()
        while self.prompt_update_eval:
            self.update_entry()

        # 3. Analyze entries
        self.analyze_status = self._get_analyze_or_exit()
        if self.analyze_status:
            self.compare_entries()

        # 4. Set reminders
        self._prompt_later_eval()

        return None

    def _check_update_eval(self):
        response = input("Would you like to update an entry? (y or n)\n")
        response = self._handle_yes_no_input(response)

        return True if response == "yes" else False

    def _load_score_params(self) -> dict:
        """loads the score params from the json file"""

        score_params_path = os.path.join(BASE_DIR, "data", "score_params.json")

        score_params = pd.read_json(score_params_path)

        score_params_dict = score_params.to_dict()

        # drop na values
        score_params_dict = remove_nulls(score_params_dict)

        return score_params_dict

    def _load_rank_params(self) -> dict:
        """loads the ranking params from the json file"""

        rank_params_path = os.path.join(BASE_DIR, "data", "rank_params.json")

        rank_params = pd.read_json(rank_params_path)

        rank_params_dict = rank_params.to_dict()

        # drop na values
        rank_params_dict = remove_nulls(rank_params_dict)

        return rank_params_dict

    def _get_name(self) -> str:
        """requests a name"""

        first = input("first name: ")
        last = input("last name: ")

        return f"{first.lower()}_{last.lower()}"

    def _create_prompt(self, key: str, max_val: int, total_length: int = 40) -> str:
        # calculate how many dashes are needed to reach the desired total length
        num_dashes = total_length - len(key) - len(f"0 to {max_val}: ")

        # ensure the number of dashes is not negative
        dashes = "-" * max(num_dashes, 1)

        # construct the prompt string
        prompt = f"{key}{dashes}0 to {max_val}: "
        return prompt

    def _get_score_results(self, update: bool = False) -> dict:
        """prompts a score value for each input"""

        entries_needed = self.score_params[self.eval_type]

        results = {}

        if update:
            results = self._load_score_results(self.eval_name)

        print("Please rank the following. Guess what you don't know, or type skip:")
        for key, max_val in entries_needed.items():

            # TESTING #
            if self.fast_test:
                results[key] = 2
                continue

            prompt = self._create_prompt(key, max_val)
            response = input(prompt)
            if response.lower() == "skip":
                continue
            else:
                response = float(response)
            while not (isinstance(response, float) & (response < max_val)):
                print(f"please enter a numeric value < {max_val}, or type 'skip'")
                response = input(prompt)

            results[key] = response

        return results

    def _get_eval_type(self) -> str:
        """request type from user"""
        response = input(f"Is this an initial eval? (y or n)\n")
        response = self._handle_yes_no_input(response)

        if response == "yes":
            return "initial"

        check_eval_response = input(f"Is this a relationship eval? (y or n)\n")
        check_eval_response = self._handle_yes_no_input(check_eval_response)

        if check_eval_response == "yes":
            return "relationship"

        print(f"The only options are {self.eval_types}")
        self._get_eval_type()

    def _get_current_evaluees(self):
        evaluees = os.listdir(self.user_dir)

        return evaluees

    def _handle_yes_no_input(self, str_to_eval: str) -> str:
        """handle yes no input"""

        while str_to_eval.lower() not in ["y", "n", "yes", "no"]:
            str_to_eval = input("invalid input. please enter 'y' or 'n'")
            str_to_eval = str_to_eval.lower()

        if str_to_eval == "y":
            str_to_eval = "yes"
        if str_to_eval == "n":
            str_to_eval = "no"

        y_or_n = str_to_eval

        return y_or_n

    def _get_analyze_or_exit(self) -> bool:
        """ask the user whether they want to analyze multiple results or exit"""

        response = input("Would you like to analyze your results? (y or n)\n")
        response = self._handle_yes_no_input(response)

        return True if response == "yes" else False

    def _prompt_later_eval(self):
        """Asks the user if they would like a reminder about updating their results"""
        later_eval = input("Need a reminder to complete a later eval? (y or n)\n")
        later_eval = self._handle_yes_no_input(later_eval)

        if later_eval == "yes":
            self.later_eval = True
        else:
            print("Thanks! exiting...")

        return None

    def _load_score_results(self):
        """loads prior score results file to allow for updates"""
        pass
        # needs to be built once final score format is finalized

    def _check_another_reponse(self):
        response = input(f"Would you like to add a new Entry? (y or n)\n")
        response = self._handle_yes_no_input(response)

        return True if response == "yes" else False

    def compare_entries(self):
        """TODO: load all entered files, evaluate total scores, and eval metrics"""
        print("comparing entries")
        pass

    def new_entry(self):
        print("Great! Please enter the person's name:\n")
        if self.fast_test:
            self.eval_name = "test_user"
        else:
            self.eval_name = self._get_name()

        if self.fast_test:
            self.eval_type = "initial"
        else:
            self.eval_type = self._get_eval_type()

        self.score_results = self._get_score_results()

        print("Thanks! evaluating results")
        self._calculate_score()

        self.eval_rank = self._calculate_rank()

        self.eval_status = self.rank_params["descriptions"][self.eval_rank]

        self._save_results()

        self.prompt_new_entry = self._check_another_reponse()

    def update_entry(self):
        """update a previous entry file"""
        print("Great! Which persons file would you like to update?:\n")
        self.eval_name = self._get_name()

        self.eval_type = self._get_eval_type()

        self.score_results = self._get_score_results()

        self._calculate_score()

        self.eval_rank = self._calculate_rank()

        self.eval_status = self.rank_params["descriptions"][self.eval_rank]

        self._save_results()

        self.prompt_new_entry = self._check_another_reponse()

    def _calculate_rank(self):
        """churns dict to find right rank"""

        # update ranking to account for potentially skipped metrics
        updated_ranking = {}
        for key, percent in self.rank_params["ranking"].items():
            updated_ranking[key] = (percent * self.max_score) / 100

        self.rank_params["ranking"] = updated_ranking

        for key, value in updated_ranking.items():
            if self.score < value:
                return key

    def _save_results(
        self,
    ) -> None:
        eval_results_path = os.path.join(
            self.user_dir, f"{self.eval_name}_{self.eval_type}_{date.today()}.csv"
        )

        if self.prompt_update_eval:
            if self.eval_type == "initial":
                print("adding new initial assessment")
            elif self.eval_type == "relationship":
                print("adding new relationship assessment")
        else:
            print(f"creating new file for {self.eval_name}")

        title = f"# Date: {date.today()}\n# User: {self.users_name}\n# Evaluee: {self.eval_name}"
        score = f"# Score: {self.score} / {self.max_score}"
        score_percent = f"# Score Percent: {self.score_percent}"
        rank = f"# Rank: {self.eval_rank}"
        status = f"# Status: {self.eval_status}"

        full_title = f"{title}\n{score}\n{score_percent}\n{rank}\n{status}"

        self.score_results["scorePercent"] = self.score_percent
        self.score_results["rank"] = self.eval_rank

        results_df = pd.DataFrame.from_dict(
            self.score_results, orient="index"
        ).reset_index()

        results_df.columns = ["trait", "score"]

        # save to file
        with open(eval_results_path, "w", newline="") as f:
            f.write(full_title + "\n")
            results_df.to_csv(f, index=False)

        print(f"{self.eval_type} results saved to: {eval_results_path}")

        return None

    def _calculate_score(self):
        """sum the values"""

        total_score = sum(self.score_results.values())
        max_score = 0

        for key, potential in self.score_params[self.eval_type].items():
            if key in self.score_results.keys():
                max_score += potential

        if total_score > max_score:
            raise ValueError("You either found THE ONE, or there was a calc error")

        self.max_score = max_score
        self.score = total_score

        self.score_percent = round((self.score / self.max_score) * 100, 2)

        return total_score


def remove_nulls(dict_all: dict) -> dict:
    """
    recursively removes keys with None or NaN values from a nested dictionary
    """
    # error check
    if dict_all is not None and not isinstance(dict_all, dict):
        raise TypeError("dict_all must be a dict")

    # create a new dictionary to avoid modifying the original during iteration
    new_dict = {}

    for k, v in dict_all.items():
        # if the value is a dictionary, apply the function recursively
        if isinstance(v, dict):
            nested_dict = remove_nulls(v)
            if nested_dict:  # only add non-empty nested dictionaries
                new_dict[k] = nested_dict
        # if the value is not None or NaN, add it to the new dictionary
        elif pd.notna(v):
            new_dict[k] = v

    return new_dict


if __name__ == "__main__":
    gfps = GFPS()

    gfps.main()
