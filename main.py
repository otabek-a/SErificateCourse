def get_movie_data(movie_title):
    """
    Fetch movie data from OMDb API
    Args:
        movie_title (str): The title of the movie to search for
    Returns:
        dict: JSON response containing movie information
    """
    base_url = "http://www.omdbapi.com/"
    movie_title = movie_title.strip()  
    params = {
        "t": movie_title,
        "r": "json",
        "apikey": "abcd1234"
    }
    print(f"Querying OMDb with params: {params}")
    
    # Ensure cache usage
    response = requests_with_caching.get(base_url, params=params)
    
    if response is None:
        raise ValueError(f"Movie not found in cache: {movie_title}")
    
    return response.json()








import re
def haha_me(movie_name: str, verbosity=0) -> str:
    movie_data = get_movie_data(movie_name)
    
    if movie_data.get("Response") == "False":
        return f"No movie found: {movie_name}"
    
    rating = rt_rating(movie_data)
    plot = movie_data.get("Plot", "No plot available.")
    joke_keyword, jokes = get_jokes(plot)
    
    if joke_keyword is None or not jokes:
        return "I've got no jokes about this movie. It's too serious!"
    
    rating_text = (
        "Hope you like them!" if rating == -1 else 
        "Hope they're better than the movie!" if rating < 70 else 
        "Hope they're as good as the movie!"
    )
    
    match = re.search(rf'\b{re.escape(joke_keyword)}\b', plot, flags=re.IGNORECASE)
    joke_keyword_original = match.group(0) if match else joke_keyword
    
    plot_highlighted = highlight(joke_keyword_original, plot)
    
    if isinstance(jokes, list):
        jokes_string = "\n".join([highlight(joke_keyword_original, joke) for joke in jokes])
    else:
        jokes_string = highlight(joke_keyword_original, jokes)
    
    result = f"""{movie_name}
Rotten Tomatoes rating: {rating}%
{plot_highlighted}
Speaking of **{joke_keyword_original}**, that reminds me of some jokes.
{rating_text}

{jokes_string}"""
    
    return result.strip()






def get_jokes(plot: str, verbosity=0) -> tuple[str, list[str]]:
    words = plot.split()  
    words = [w.strip(",.!;:") for w in words]  # Punktuatsiyani olib tashlash
    
    words = sorted(words, key=len, reverse=True)  # So‘zlarni uzunligi bo‘yicha kamayish tartibida saralash

    for word in words:
        if verbosity:
            print(f"Trying word: {word}")
        joke_data = get_joke_data(word)
        if joke_data.get("results"):
            jokes = [joke["joke"] for joke in joke_data["results"]]
            return word, jokes

    return None, None












# no template is provided for this function. You have to define it from scratch

def get_joke_data(search_term: str) -> dict:
    """
    Fetches jokes related to the given search term from the icanhazdadjokes API.
    
    Args:
        search_term (str): The word to search jokes for.
    
    Returns:
        dict: The API response containing jokes or an empty result.
    """
    parameters = {"term": search_term, "limit": 2}
    response = requests_with_caching.get("https://icanhazdadjoke.com/search", params=parameters, headers={"Accept": "application/json"})
    return response.json()






def rt_rating(movie_data: dict) -> int:
    """Returns the Rotten Tomatoes rating from a dictionary of movie information.

    Parameters
    ----------
    movie_data : dict
        A dictionary of movie information.

    Returns
    -------
    int
        The Rotten Tomatoes rating. For example, 75% would be returned as the integer 75.
    """
    retings = movie_data['Ratings'][1]
    if retings.get("Source") == "Rotten Tomatoes":
        value = retings['Value'].replace('%', '')
        return int(value)
    else:
        return -1