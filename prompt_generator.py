import json
import re
import base64

# Define allowed encodings per template tag
ALLOWED_ENCODINGS = {
    "AIM": ["origin", "compressed", "leetspeak", "unicode", "fragments", "base64", "rot13"],
    "Compress": ["compressed"],
    "Fragments": ["fragments"],
    "Base64_Base64": ["base64"],
    "Base64_NL": ["base64"],
    "NL_Base64": ["origin", "compressed", "leetspeak", "unicode", "fragments", "base64", "rot13"],
    "ROT13": ["rot13"],
    "DevMode": ["origin", "compressed", "leetspeak", "unicode", "fragments", "base64", "rot13"],
    "Wiki": ["origin", "compressed", "leetspeak", "unicode", "fragments", "base64", "rot13"],
    "Injection_1": ["origin", "compressed", "leetspeak", "unicode", "fragments", "base64", "rot13"],
    "Injection_2": ["origin", "compressed", "leetspeak", "unicode", "fragments", "base64", "rot13"],
    "Injection_3": ["origin", "compressed", "leetspeak", "unicode", "fragments", "base64", "rot13"],
    "JSON_1": ["origin", "compressed", "leetspeak", "unicode", "fragments", "base64", "rot13"],
    "JSON_2": ["origin", "compressed", "leetspeak", "unicode", "fragments", "base64", "rot13"],
    "Prefix_1": ["origin", "compressed", "leetspeak", "unicode", "fragments", "base64", "rot13"],
    "Prefix_2": ["origin", "compressed", "leetspeak", "unicode", "fragments", "base64", "rot13"],
    "Rule_1": ["origin", "compressed", "leetspeak", "unicode", "fragments", "base64", "rot13"],
    "Rule_2": ["origin", "compressed", "leetspeak", "unicode", "fragments", "base64", "rot13"],
    "Prefix_Rule_1": ["origin", "compressed", "leetspeak", "unicode", "fragments", "base64", "rot13"],
    "Prefix_Rule_2": ["origin", "compressed", "leetspeak", "unicode", "fragments", "base64", "rot13"],
}

# Encoding functions
ENCODINGS = {
    "origin": lambda x: x,
    "compressed": lambda x: encode_compress_string(x),
    "leetspeak": lambda x: leetspeak_encoding(x),
    "unicode": lambda x: leetspeak_unicode_encoding(x),
    "fragments": lambda x: encode_with_word_fragments(x),
    "base64": lambda x: base64_encoding(x),
    "rot13": lambda x: rot13_encoding(x),
}

def load_templates(file_path):
    """Load templates from a JSONL file."""
    templates = []
    with open(file_path, "r") as file:
        for line in file:
            if line.strip():
                data = json.loads(line)
                templates.append(data)
    return templates


def save_to_output(data, file_path):
    """Write formatted prompts to a JSONL file."""
    with open(file_path, "w") as file:
        for entry in data:
            file.write(json.dumps({"prompt": entry}) + "\n")


def generate_prompts(user_input, templates):
    """
    Generate prompts using user input, templates, and encoded variations of the input.

    Args:
        user_input (str): The original user input to encode and use in prompts.
        templates (list): A list of template dictionaries.

    Returns:
        list: A list of all generated prompts.
    """
    generated_prompts = []
    for template in templates:
        template_tag = template.get("tag", "")  # Get the tag of the template
        prompt_template = template.get("template", "")

        # Add the original prompt as a baseline
        try:
            original_prompt = prompt_template.format(user_input=user_input)
            generated_prompts.append({"tag": template_tag, "encoding": "origin", "prompt": original_prompt})
        except KeyError as e:
            print(f"Error formatting original prompt: {e}")
            continue

        # Get allowed encodings for this template
        allowed_encodings = ALLOWED_ENCODINGS.get(template_tag, [])

        for encoding_name, encoder in ENCODINGS.items():
            if encoding_name not in allowed_encodings or encoding_name == "origin":
                # Skip encodings not allowed or already handled as baseline
                continue

            try:
                # Apply encoding to the user input
                encoded_input = encoder(user_input)
                # Replace {user_input} in the template
                prompt = prompt_template.format(user_input=encoded_input)
                generated_prompts.append({"tag": template_tag, "encoding": encoding_name, "prompt": prompt})
            except KeyError as e:
                print(f"Error formatting template: {e}")
                print(f"Problematic template: {prompt_template}")
            except Exception as e:
                print(f"Unexpected error: {e}")
                print(f"Encoder: {encoding_name}, Input: {user_input}")

    return generated_prompts

##### Encoders
def encode_compress_string(input_string):
    """
    Compresses a string by removing vowels from each word, except for the first letter.
    This method generalizes the compression to any input text without relying on predefined words.
    
    Args:
        input_string (str): The original string to compress.
    
    Returns:
        str: The compressed string.
    """
    # Regular expression to match words
    words = input_string.split()
    
    # Function to remove vowels except for the first character
    def compress_word(word):
        return word[0] + re.sub(r'[aeiouAEIOU]', '', word[1:])
    
    # Apply compression to each word
    compressed_words = [compress_word(word) for word in words]
    
    # Join the processed words back into a single string
    return ' '.join(compressed_words)

def leetspeak_encoding(input_string):
    """
    Encodes a string into leetspeak by replacing letters with numeral or symbolic equivalents.
    
    Args:
        input_string (str): The original string to encode.
    
    Returns:
        str: The encoded string in leetspeak.
    """
    # Mapping of characters to their leetspeak equivalents
    char_map = {
        'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7',
        'A': '4', 'E': '3', 'I': '1', 'O': '0', 'S': '5', 'T': '7'
    }

    # Encode each character in the input string using the mapping
    encoded_string = ''.join(char_map.get(char, char) for char in input_string)

    return encoded_string

def leetspeak_unicode_encoding(input_string):
    """
    Encodes a string into a stylized leetspeak format with Unicode subscripts.
    
    Args:
        input_string (str): The original string to encode.
    
    Returns:
        str: The encoded string.
    """
    # Mapping of characters to their leetspeak and Unicode subscript equivalents
    char_map = {
        'a': '4', 'b': '8', 'c': '\u20e3c', 'd': '\u20e3d', 'e': '3',
        'f': '\u20e3f', 'g': 'g\u20e3', 'h': '\u20e3h', 'i': '1',
        'j': '\u20e3j', 'k': '\u20e3k', 'l': 'l\u20e3', 'm': '\u20e3m',
        'n': 'n\u20e3', 'o': '0\u20e3', 'p': '\u20e3p', 'q': '\u20e3q',
        'r': '\u20e3r', 's': '\u20e3s', 't': '7', 'u': 'U\u20e3',
        'v': 'V', 'w': '\u20e3w', 'x': '\u20e3x', 'y': '\u20e3y', 'z': '\u20e3z',
        'A': '4', 'B': '8', 'C': '\u20e3C', 'D': '\u20e3D', 'E': '3',
        'F': '\u20e3F', 'G': 'G\u20e3', 'H': '\u20e3H', 'I': '1',
        'J': '\u20e3J', 'K': '\u20e3K', 'L': 'L\u20e3', 'M': '\u20e3M',
        'N': 'N\u20e3', 'O': '0\u20e3', 'P': '\u20e3P', 'Q': '\u20e3Q',
        'R': '\u20e3R', 'S': '\u20e3S', 'T': '7', 'U': 'U\u20e3',
        'V': 'V', 'W': '\u20e3W', 'X': '\u20e3X', 'Y': '\u20e3Y', 'Z': '\u20e3Z'
    }

    # Encode each character in the input string using the mapping
    encoded_string = ''.join(char_map.get(char, char) for char in input_string)

    return encoded_string

def encode_with_word_fragments(input_string):
    """
    Encodes a string by splitting specific words into fragments and creating reconstruction instructions
    using named variables and concatenation with '+'.
    
    Args:
        input_string (str): The original string to encode.
    
    Returns:
        str: The encoded message in the specified format.
    """
    # Helper function to split a word into fragments
    def split_word(word):
        n = len(word)
        return [word[:n // 3], word[n // 3: 2 * n // 3], word[2 * n // 3:]]
    
    # List to store the encoded variables
    variables = []
    # List to construct the output template
    template = []
    # Variable counter
    counter = 0

    for word in input_string.split():
        if len(word) > 3:  # Split words longer than 3 characters
            fragments = split_word(word)
            fragment_vars = []
            for fragment in fragments:
                var_name = f"z_{counter}"
                variables.append(f"{var_name} = {fragment}")
                fragment_vars.append(var_name)
                counter += 1
            # Append the reconstructed word using '+' for concatenation
            template.append(f"{{{' + '.join(fragment_vars)}}}")
        else:
            # Leave short words (like stop words) as they are
            template.append(word)
    
    # Combine the variable definitions and the reconstruction template
    encoded_message = "\n".join(variables) + "\n\n" + " ".join(template)

    return encoded_message

def base64_encoding(input_string):
    """
    Encodes a string into a Base64 encoded string.
    
    Args:
        input_string (str): The original string to encode.
    
    Returns:
        str: The Base64 encoded string.
    """
    # Convert the input string to bytes
    input_bytes = input_string.encode('utf-8')
    # Encode the bytes to Base64
    encoded_bytes = base64.b64encode(input_bytes)
    # Convert the Base64 bytes back to a string
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string

def rot13_encoding(input_string):
    """
    Encodes a string using the ROT13 cipher.
    Each letter is shifted by 13 places in the alphabet, preserving case.
    
    Args:
        input_string (str): The original string to encode.
    
    Returns:
        str: The ROT13 encoded string.
    """
    # Define the ROT13 transformation
    def shift_char(char):
        if 'a' <= char <= 'z':  # Lowercase letters
            return chr((ord(char) - ord('a') + 13) % 26 + ord('a'))
        elif 'A' <= char <= 'Z':  # Uppercase letters
            return chr((ord(char) - ord('A') + 13) % 26 + ord('A'))
        else:
            return char  # Non-alphabetic characters remain unchanged

    # Apply the transformation to each character in the string
    return ''.join(shift_char(char) for char in input_string)

def main():
    template_file = "data/templates.jsonl"
    output_file = "data/output.jsonl"
    user_input = input("Enter the malicious input to craft prompts: ")

    print("Loading templates...")
    templates = load_templates(template_file)
    print(f"Loaded {len(templates)} templates.")

    print("Generating prompts...")
    generated_prompts = generate_prompts(user_input, templates)

    print(f"Writing {len(generated_prompts)} prompts to {output_file}...")
    save_to_output(generated_prompts, output_file)
    print("Finished! The prompts have been saved.")

if __name__ == "__main__":
    main()