from flask import Flask, request, jsonify
import scrapetube
import json

app = Flask(__name__)

def buscar_streams_yt(url):
    try:
        videos = scrapetube.get_channel(channel_url=url, content_type='streams', sort_by='newest')
        videos_data = []
        for video in videos:
            if "upcomingEventData" not in video:
                objeto = {
                    "id": video["videoId"],
                    "channelId": url,
                    "liveChatId": None,
                    "title": video["title"]["runs"][0]["text"],
                    "description": None,
                    "publishedAt": None,
                    "scheduledStartTime": None,
                    "actualStartTime": None,
                    "actualEndTime": None
                }
                videos_data.append(objeto)
        return json.dumps(videos_data, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@app.route('/buscar-streams', methods=['GET'])
def buscar_streams():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "O parâmetro 'url' é obrigatório"}), 400
    resultado = buscar_streams_yt(url)
    return jsonify(json.loads(resultado))

if __name__ == '__main__':
    app.run(debug=True)