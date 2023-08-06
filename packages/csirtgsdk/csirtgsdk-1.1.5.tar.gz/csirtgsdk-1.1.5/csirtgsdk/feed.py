from csirtgsdk.client.http import HTTP as Client


class Feed(object):
    """
    Represents a Feed Object
    """
    def __init__(self, client=Client()):
        self.client = client

    def get_lines(self, data):
        from prettytable import PrettyTable
        cols = ['name', 'description', 'license', 'updated_at']
        t = PrettyTable(cols)
        if isinstance(data, dict):
            data = [data]

        for f in data:
            r = []

            for c in cols:
                y = f.get(c)
                if c == 'license':
                    y = y['name']
                y = str(y)
                y = (y[:30] + '..') if len(y) > 30 else y
                r.append(y)
            t.add_row(r)

        yield str(t)

    def new(self, user, name, description=None):
        """
        Creates a new Feed object

        :param user: feed username
        :param name: feed name
        :param description: feed description
        :return: dict
        """
        uri = self.client.remote + '/users/{0}/feeds'.format(user)

        data = {
            'feed': {
                'name': name,
                'description': description
            }
        }

        resp = self.client.post(uri, data)
        return resp

    def delete(self, user, name):
        """
        Removes a feed

        :param user: feed username
        :param name: feed name
        :return: true/false
        """

        uri = self.client.remote + '/users/{}/feeds/{}'.format(user, name)

        resp = self.client.session.delete(uri)
        return resp.status_code

    remove = delete

    def index(self, user):
        """
        Returns a list of Feeds from the API

        :param user: feed username
        :return: list

        Example:
            ret = feed.index('csirtgadgets')
        """
        uri = self.client.remote + '/users/{0}/feeds'.format(user)
        return self.client.get(uri)

    def show(self, user, name, limit=None, lasttime=None):
        """
        Returns a specific Feed from the API

        :param user: feed username
        :param name: feed name
        :param limit: limit the results
        :param lasttime: only show >= lasttime
        :return: dict

        Example:
            ret = feed.show('csirtgadgets', 'port-scanners', limit=5)
        """
        uri = self.client.remote + '/users/{0}/feeds/{1}'.format(user, name)
        return self.client.get(uri, params={'limit': limit, 'lasttime': lasttime})
