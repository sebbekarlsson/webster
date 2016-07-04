from webster.web.SpiderNet import SpiderNet


if __name__ == '__main__':
    net = SpiderNet()
    net.start(
                [
                    'http://www.ica.se/',
                    'https://www.coop.se/',
                    'http://duva.se/',
                    'http://www.ember.se/',
                    'https://lidkoping.se/',
                    'https://www.flashback.org/',
                    'https://sv.wordpress.org/',
                    'http://www.gotene.se/index.html'
                ]
            )
