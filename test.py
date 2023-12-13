import openai
import subprocess
import re

# Your OpenAI API key
openai.api_key = "YOUR_API_KEY"

def is_safe_command(command):
    # Implement safety checks here
    unsafe_patterns = ["rm ", "sudo", ":(){:|:&};:"]
    return not any(pattern in command for pattern in unsafe_patterns)


def run_shell_command(command):
    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        return (
            result.stdout
            or "Command executed successfully, but no output was returned."
        )
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e}"


def main():
    while True:
        user_input = input("You: ")
        prompt = f"Run this shell command: '{user_input}'"

        # Get response from GPT-4
        response = openai.Completion.create(
            engine="text-davinci-003", prompt=prompt, max_tokens=100
        )

        command = response.choices[0].text.strip()

        if is_safe_command(command):
            print("Executing:", command)
            output = run_shell_command(command)
            print("Output:", output)
        else:
            print("Unsafe command detected, not executing.")


if __name__ == "__main__":
    main()
