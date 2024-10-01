from openai import OpenAI
import openai

client = OpenAI()


def gptUseCultures(chunk, verbose=False):
    if verbose:
        print("Analyzing chunk for cell cultures...")
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a precise and accurate assistant specialized in identifying human cell types from scientific texts."},
                {"role": "user", "content": f"Analyze the following article text and extract a list of human cell types (cell lines or primary cell cultures only):\n\n{chunk}"},
                {"role": "assistant", "content": "I will provide a comma-separated list of human cell types (cell lines or primary cell cultures) mentioned in the text. I will exclude human names, department names, and university names. If no relevant cell types are found, I will return a single hyphen (-). I will aim to find at least 20 cell types if possible. I will just return a comma separated list of cell types and no other text."}
            ]
        )
        result = completion.choices[0].message.content
        if verbose:
            print(f"Found cell cultures: {result}")
        return result
    except openai.BadRequestError as e:
        if verbose:
            print(f"Error in gptUseCultures: {str(e)}")
        return ""


def gptUseEthnicities(chunk, cultures, verbose=False):
    if verbose:
        print("Analyzing chunk for ethnicities...")
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a precise and accurate assistant specialized in identifying human races and nationalities from scientific texts."},
                {"role": "user", "content": f"Analyze the following article text and extract a list of human races or nationalities mentioned:\n\n{chunk}\n\nFor context, these cell cultures were found in the text: {cultures}"},
                {"role": "assistant", "content": "I will provide a comma-separated list of human races or nationalities mentioned in the text. I will exclude human names, department names, and university names. If no relevant races or nationalities are found, I will return a single hyphen (-)."}
            ]
        )
        result = completion.choices[0].message.content
        if verbose:
            print(f"Found ethnicities: {result}")
        return result
    except openai.BadRequestError as e:
        if verbose:
            print(f"Error in gptUseEthnicities: {str(e)}")
        return ""


def gptForPrimaryCellCultures(culture, text, verbose=False):
    if verbose:
        print("Analyzing text for primary cell cultures...")
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a precise and accurate assistant specialized in identifying the ancestry of cell cultures from scientific texts."},
                {"role": "user", "content": f"In the following text, identify the ancestry (human race or nationality) of this cell culture: {culture}\n\nText: {text}"},
                {"role": "assistant", "content": "I will return a single word representing the race or nationality of the specified cell culture, exactly as it appears in the text. If the ancestry is not mentioned or cannot be determined, I will return a hyphen (-)."}
            ]
        )
        result = completion.choices[0].message.content
        if verbose:
            print(f"Found ancestry: {result}")
        return result
    except openai.BadRequestError as e:
        if verbose:
            print(f"Error in gptForPrimaryCellCultures: {str(e)}")
        return "-"

def filterHyphenResult(result):
    if result.strip().lower() in ['-', 'hyphen', '(-)', '- ']:
        return ""
    return result


def gptFilterList(text, l, verbose=False):
    if verbose:
        print("Filtering list...")
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a precise and accurate assistant specialized in filtering and refining lists based on specific criteria."},
            {"role": "user", "content": f"Filter the following list to include only items related to {text}:\n\n{l}"},
            {"role": "assistant", "content": f"I will provide a comma-separated list of items from the given list that are directly related to {text}. I will exclude names, university names, department names, and irrelevant strings. I will maintain the original spelling and formatting of the relevant items. I will be thorough in my analysis to ensure no relevant items are missed. I will just return a comma separated list of cell types and no other text."}
        ]
    )
    result = completion.choices[0].message.content
    if verbose:
        print(f"Filtered list: {result}")
    return result

