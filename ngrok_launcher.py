from pyngrok import ngrok

def start_ngrok(port=4046):
    """
    Starts ngrok to expose the Streamlit app to the internet.
    Returns the public URL.
    """
    public_url = ngrok.connect(port).public_url
    return public_url
