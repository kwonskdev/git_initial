import re
import sys


def get_type_list(commit_template="./commit_template"):
    with open(commit_template, "r", encoding="UTF8") as f:
        type_list = []
        lines = f.readlines()

        for idx, line in enumerate(lines):
            if line == "# 새로운 타입이 필요할 경우 아래에 추가 \n":
                type_start_index = idx + 1
                break

        for line in lines[type_start_index:]:
            if line == "################\n":
                break
            type_list.append(line.split(" : ")[0][2:])

        return type_list


def check_commit_template():
    error_msgs = []
    type_list = get_type_list()

    type_regex = re.compile(".*(?=\s:)")
    title_regex = re.compile("(?<=:\s).*")
    body_regex = re.compile("(?<=-\s).*")

    with open(sys.argv[1], "r", encoding="UTF8") as commit:
        lines = commit.readlines()
        lines = [line for line in lines if not line.startswith("#")]
        while lines[-1] == "\n":
            lines = lines[:-1]
            if len(lines) == 0:
                break

        if (type_regex.search(lines[0]) is None) or (title_regex.search(lines[0]) is None):
            error_msgs.append("Title must be 'type : title'.")

        if type_regex.search(lines[0]):
            if type_regex.search(lines[0]).group() not in type_list:
                error_msgs.append(f"Type must be in {type_list}")

        if len(lines[0]) > 50:
            error_msgs.append("Title must be under 50 characters.")

        if len(lines) < 3:
            error_msgs.append("Commit message must include body.")
        else:
            if lines[1] != "\n":
                error_msgs.append("There must be and blank line between title and body")
            for line in lines[2:]:
                if body_regex.search(line) is None:
                    error_msgs.append(
                        "Body message must start with '-.'"
                        + "And blank can be front of '-'."
                        + f"But your body is '{line}'."
                    )

    if len(error_msgs) > 0:
        print("----------CHECKING COMMIT MESSAGE----------\n")
        for idx, error_msg in enumerate(error_msgs):
            print(f"[{idx}] {error_msg}")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    check_commit_template()
