import tekore as tk
def authorize():
    CLIENT_ID = "fc98ccddf3be4fd9a533322840618317"
    CLIENT_SECRET = "1dd9e383af0645d89458a90ef33eff13"
    app_token = tk.request_client_token(CLIENT_ID, CLIENT_SECRET)
    return tk.Spotify(app_token)