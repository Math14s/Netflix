from flask import Flask, render_template, abort

app = Flask(__name__)

series_data = {
    'poster': '/static/serie.jpg',
    'seasons': {
        1: {
            'folder': 'https://drive.google.com/drive/folders/1-UUhp0c1Bl8RKE17X0CbmqHOBXooRjon',
            'episodes': {
                1: '1-1KACy2FpM67tfAGOPUZ7Zl6jdt0mrAD',
                2: '1-1olokkBpRjpS0ZmurQRwrWaQ8F8UN7o',
                3: '1-95TD9N2VpayKUYXm6c2N4svjfcakMIm',
                4: '1-EI3fjrO24ZV4Os1XuZGY4tAD9fXQn6p',
                5: '1-KFkpyIJldDdRRgsobezKX7Z_YaB7yWm',
                6: '1-M3IwlllpqajhmC46zFRl1nql32qmsu-'
            }
        },
        2: {
            'folder': 'https://drive.google.com/drive/folders/1Ij2HAXz3TUUr6chkdr09B649_ehi_mWF',
            'episodes': {
                1: '1sUsEsMO5BgmVRv1wK5BtEhC51WfVoa6r',
                2: '1zmmYk0QylypkY9gdz4ZgUvsOKEy-WGvB',
                3: '1-x5_jbvURVg0dGoQVK2zNlGQGCezOqh5',
                4: '1Uihwy_kxWJiAeYhkSaFUgZLKMvuJjkAv',
                5: '1y1O0evLIRxeBW8imr_WlsoTK2pr7YfRq',
                6: '1pZWNo9Yfki7cfwJwlLsDO3cQ9ddE7Rw3',
                7: '1ejLdjvpoaO09JnhrVf68xr6rdIXm_Fqf'
            }
        },
        3: {
            'folder': 'https://drive.google.com/drive/folders/113RuMH9FS-qYKHOhEVWKUi3LsRLD9Jmm',
            'episodes': {
                1: '11fgdtqJ3NRgvN4dMdI-Uj-ZTACguNZgA',
                2: '11iXHCnCbQoulx-c_be-WNavoCEiFVlmu',
                3: '11lZuuCKaxjXUBhCY0kS4osBtyI3c4RLJ',
                4: '11nO4jaQZ1wyO1NeNv5dJTkj0dfSqo7OU',
                5: '11uhTMmp_EQOjZY78GBjQyglJagCoy0_2',
                6: '11zngZEzfgfkZ5DkPx4Rl6j-6u-wevhMZ',
                7: '12-eHGQraQkBxJw6IMOW_RFCb6WBw6dEy',
                8: '125B3klbk31MfxjgbPXx9Ne18Me7IgjN0',
                9: '12621XQL7RriCvX9Mwv7fJMddHs03_UcP',
                10: '12IvEh_ACLwp8cWUO0nWAjwlfvxE1C9gO'
            }
        },
        4: {
            'folder': 'https://drive.google.com/drive/folders/12PMJMA64rqc4YBssVDYVkFypxEh7rVuJ',
            'episodes': {
                1: '12agQS_n9dkMqV_y4dCm1jMgJNpuKvmJm',
                2: '12dRC1BQamSwysYcwxdDxnnJSU4ieQLZq',
                3: '12fdjbt4YIqFF66Lxy30gGevCjVkn1UEj',
                4: '12jq7I46hMbhUhYr8Sl96ID5ZgJVzLKUp',
                5: '12tdGfKFrrgtJr4KrQ4HH504fq4R7B5K5',
                6: '12zpsS4DsiGKJ6p0w1qzyowZ4ZloPpEIh',
                7: '132r9CLD3lYpCPvCdDZNYRPzXsxKw-z6Q'
            }
        },
        5: {
            'folder': 'https://drive.google.com/drive/u/0/folders/11R-Yr9zvLnr_NPnruaB7wVcw_5GLUDjk',
            'episodes': {
                1: '11Vy1Hplk8Wow7N256Y0NVFlCKvLiqNg8',
                2: '11fINws4zwJ9h0DT3zrfO8SUqbAwc6ElX',
                3: '11jO9P9Dc0QKfBynNtf2AHhXFKI_YjULG',
                4: '124uw6xmnfNOQiv7VTT5YNwdRLgJPJWoo',
                5: '12GCgShFUU4cl_ZkBUuqQWHzoxB4FUL0u',
                6: '12Jg2XFnlmVnW6heQpAn7dMvtScvyoDLr'
            }
        }
    }
}

@app.route('/')
def index():
    return render_template('index.html', poster=series_data['poster'])

@app.route('/seasons')
def seasons():
    return render_template('seasons.html', seasons=series_data['seasons'])

@app.route('/player/<int:season>/<int:episode>')
def player(season, episode):
    season_data = series_data['seasons'].get(season)
    if not season_data:
        abort(404)
    
    episodes = season_data['episodes']
    if episode not in episodes:
        abort(404)
    
    # Lógica de navegação
    episode_numbers = sorted(episodes.keys())
    current_index = episode_numbers.index(episode)
    
    next_episode = None
    next_season = None
    first_episode_next_season = None
    
    # Verifica próximo episódio
    if current_index + 1 < len(episode_numbers):
        next_episode = episode_numbers[current_index + 1]
    else:
        # Verifica próxima temporada
        season_numbers = sorted(series_data['seasons'].keys())
        current_season_index = season_numbers.index(season)
        if current_season_index + 1 < len(season_numbers):
            next_season = season_numbers[current_season_index + 1]
            first_episode_next_season = sorted(series_data['seasons'][next_season]['episodes'].keys())[0]

    video_url = f"https://drive.google.com/file/d/{episodes[episode]}/preview"
    
    return render_template(
        'player.html',
        video_url=video_url,
        season=season,
        next_episode=next_episode,
        next_season=next_season,
        first_episode_next_season=first_episode_next_season
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)