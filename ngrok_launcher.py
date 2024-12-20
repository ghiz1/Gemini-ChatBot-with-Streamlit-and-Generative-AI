from pyngrok import ngrok

def start_ngrok(port):
    """
    Starts ngrok to expose the Streamlit app to the internet.
    Returns the public URL.
    """
    # Check if a tunnel is already running
    existing_tunnels = ngrok.get_tunnels()
    for tunnel in existing_tunnels:
        if str(port) in tunnel.public_url:
            return tunnel.public_url

    # Start a new tunnel if none exist
    public_url = ngrok.connect(port).public_url
    print(f"ngrok tunnel started: {public_url}")
    return public_url
