import yarl
import asyncio


__all__ = ()


ENDPOINT = yarl.URL('https://discordapp.com')


AUTHORIZATION_URL = ENDPOINT.with_path('/api/oauth2/authorize')


TOKEN_URL = ENDPOINT.with_path('/api/oauth2/token')


REVOCATION_URL = ENDPOINT.with_path('/api/oauth2/token/revoke')


def process_access_token_response(data):

    refresh_at = now + data['expires_in']

    refresh_tojen = data['refresh_token']

    token_type = data['token_type']

    access_token = data['access_token']

    full_token = f'{token_type} {access_token}'

    return (full_token, refresh_token, expires_in)


async def get_access_token(session, client_id, client_secret,
                           scopes, redirect_uri, get_code):

    scope = ' '.join(scopes)

    query = {
        'response_type': 'code',
        'client_id': client_id,
        'scopes': scopes,
        'redirect_uri': redirect_uri
    }

    url = AUTHORIZATION_URL.with_query(query)

    code = await get_code(url)

    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'scope': scope
    }

    url = TOKEN_URL

    response = await session.post(url, data = data)

    data = await response.json()

    return process_access_token_response(data)


async def refresh_access_token(session, refresh_token):

    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': refresh_token,
        'refresh_token': refresh_token,
        'redirect_uri': redirect_uri,
        'scope': scope
    }

    url = TOKEN_URL

    response = await session.post(url, data = data)

    data = await response.json()

    return process_access_token_response(data)


class AuthHandle:

    def __init__(self, session):

        self._session = session

        loop = session._loop

        self._event = asyncio.Event(loop = loop)

        self._token = None

        self._loop = loop

    async def get(self):

        await self._event.wait()

        return self._token

    async def execute(self, *args):

        details = await get_access_token(self._session, *args)

        while not session.closed:

            (access, refresh, expiry) = details

            self._token = access

            self._event.set()

            await asyncio.sleep(expiry - safe)

            self._event.clear()

            details = await refresh_access_token(self._session, refresh)

    def start(self, *args):

        coroutine = self.execute(*args)

        self._task = self._loop.create_task(coroutine)

    def stop(self):

        self._task.cancel()
