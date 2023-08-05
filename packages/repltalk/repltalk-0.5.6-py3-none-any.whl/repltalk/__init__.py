import aiohttp
from datetime import datetime

# Bots approved by the Repl.it Team that are allowed to log in (100% impossible to hack definitely)
whitelisted_bots = {
	'repltalk'
}

base_url = 'https://repl.it'


class NotWhitelisted(Exception): pass


class BoardDoesntExist(Exception): pass


class GraphqlError(Exception): pass


class InvalidLogin(Exception): pass


board_ids = {
	'Share': 3,
	'Ask': 6,
	'Announcements': 14,
	'Challenge': 16,
	'Learn': 17
}


class PostList(list):
	def __init__(self, posts, board, after, sort, search):
		self.posts = posts
		self.after = after
		self.board = board
		self.sort = sort
		self.search = search

	def __iter__(self):
		self.i = 0
		return self

	def __next__(self):
		self.i += 1
		if self.i >= len(self.posts):
			raise StopIteration
		return self.posts[self.i]

	def __str__(self):
		if len(self.posts) > 30:
			return f'<{len(self.posts)} posts>'
		return str(self.posts)

	def __getitem__(self, indices):
		return self.posts[indices]

	async def next(self):
		post_list = await self.board.get_posts(
			sort=self.sort,
			search=self.search,
			after=self.after
		)
		self.posts = post_list.posts
		self.board = post_list.board
		self.after = post_list.after
		self.sort = post_list.sort
		self.search = post_list.search
		return self


class CommentList(list):
	def __init__(self, post, comments, board, after, sort):
		self.post = post
		self.comments = comments
		self.after = after
		self.board = board
		self.sort = sort

	def __iter__(self):
		self.i = 0
		return self

	def __next__(self):
		self.i += 1
		if self.i >= len(self.posts):
			raise StopIteration
		return self.comments[self.i]

	def __str__(self):
		if len(self.posts) > 30:
			return f'<{len(self.posts)} comments>'
		return str(self.posts)

	async def next(self):
		post_list = await self.board.comments(
			sort=self.sort,
			search=self.search,
			after=self.after
		)
		self.posts = post_list.posts
		self.board = post_list.board
		self.after = post_list.after
		self.sort = post_list.sort
		self.search = post_list.search


class Comment():
	def __init__(
		self, client, id, body, time_created, can_edit,
		can_comment, can_report, has_reported, url, votes,
		can_vote, has_voted, user, post, comments,
		parent=None
	):
		self.client = client
		self.id = id
		self.content = body
		self.datetime = datetime.strptime(time_created, '%Y-%m-%dT%H:%M:%S.%fZ')
		self.can_edit = can_edit
		self.can_comment = can_comment
		self.can_report = can_report
		self.has_reported = has_reported
		self.url = base_url + url
		self.votes = votes
		self.can_vote = can_vote
		self.has_voted = has_voted
		self.parent = parent
		if user is not None:
			user = User(
				client,
				user=user
			)
		self.author = user
		self.post = post  # Should already be a post object
		replies = []
		for c in comments:
			try:
				co = c['comments']
			except KeyError:
				co = []
			replies.append(Comment(
				self.client,
				id=c['id'],
				body=c['body'],
				time_created=c['timeCreated'],
				can_edit=c['canEdit'],
				can_comment=c['canComment'],
				can_report=c['canReport'],
				has_reported=c['hasReported'],
				url=c['url'],
				votes=c['voteCount'],
				can_vote=c['canVote'],
				has_voted=c['hasVoted'],
				user=c['user'],
				post=self.post,
				comments=co,
				parent=self
			))
		self.replies = replies

	def __repr__(self):
		if len(self.content) > 100:
			return repr(self.content[:100] + '...')
		else:
			return repr(self.content)

	def __eq__(self, post2):
		return self.id == post2.id

	def __ne__(self, post2):
		return self.id != post2.id

	async def reply(self, content):
		c = await self.client.perform_graphql(
			'createComment',
			graphql.create_comment,
			input={
				'body': content,
				'commentId': self.id,
				'postId': self.post.id
			}
		)
		return Comment(
			self,
			id=c['id'],
			body=c['body'],
			time_created=c['timeCreated'],
			can_edit=c['canEdit'],
			can_comment=c['canComment'],
			can_report=c['canReport'],
			has_reported=c['hasReported'],
			url=c['url'],
			votes=c['voteCount'],
			can_vote=c['canVote'],
			has_voted=c['hasVoted'],
			user=c['user'],
			post=c['post'],
			comments=c['comments']
		)


class Board():
	def __init__(self, client):
		self.client = client

	async def _get_posts(self, sort, search, after):
		if self.name == 'All':
			return await self.client._get_all_posts(
				order=sort,
				search_query='',
				after=after
			)
		else:
			if self.name in board_ids:
				board_id = board_ids[self.name]

				return await self.client._posts_in_board(
					board_id=board_id,  # :ok_hand:
					order=sort,
					search_query=search,
					after=after
				)
			else:
				raise BoardDoesntExist(f'Board "{self.name}" doesn\'t exist.')

	async def get_posts(self, sort='top', search='', after=None):
		if sort == 'top':
			sort = 'votes'
		_posts = await self._get_posts(
			sort=sort,
			search=search,
			after=after
		)
		posts = []
		for post in _posts['items']:
			posts.append(
				Post(
					self.client,
					id=post['id'],
					title=post['title'],
					body=post['body'],
					is_announcement=post['isAnnouncement'],
					url=post['url'],
					board=post['board'],
					time_created=post['timeCreated'],
					can_edit=post['canEdit'],
					can_comment=post['canComment'],
					can_pin=post['canPin'],
					can_set_type=post['canSetType'],
					can_report=post['canReport'],
					has_reported=post['hasReported'],
					is_locked=post['isLocked'],
					show_hosted=post['showHosted'],
					vote_count=post['voteCount'],
					can_vote=post['canVote'],
					has_voted=post['hasVoted'],
					user=post['user'],
					repl=post['repl']
				)
			)
		return PostList(
			posts=posts,
			board=self,
			after=_posts['pageInfo']['nextCursor'],
			sort=sort,
			search=search
		)

	def __repr__(self):
		return f'<{self.name} board>'


class RichBoard(Board):  # a board with more stuff than usual
	def __init__(self, client, id, url, slug, title_cta, body_cta, button_cta, name):
		self.id = id
		self.url = base_url + url
		self.name = name
		self.slug = slug
		self.client = client
		self.body_cta = body_cta
		self.title_cta = title_cta
		self.button_cta = button_cta


class Language():
	def __init__(
		self, name, display_name
	):
		self.name = name
		self.display_name = display_name

	def __str__(self):
		return self.display_name

	def __repr__(self):
		return f'<{self.name}>'


class Repl():
	def __init__(
		self, id, embed_url, hosted_url, title, language, language_name
	):
		self.id = id
		self.embed_url = embed_url
		self.url = hosted_url
		self.title = title
		self.language = Language(
			name=language,
			display_name=language_name
		)

	def __repr__(self):
		return f'<{self.title}>'


class Post():
	def __init__(
		self, client, id, title, body, is_announcement,
		url, board, time_created, can_edit, can_comment,
		can_pin, can_set_type, can_report, has_reported,
		is_locked, show_hosted, vote_count, can_vote,
		has_voted, user, repl
	):
		self.client = client
		self.id = id
		self.title = title
		self.content = body
		self.is_announcement = is_announcement
		self.url = base_url + url
		board = RichBoard(
			client=client,
			id=board['id'],
			url=board['url'],
			slug=board['slug'],
			title_cta=board['titleCta'],
			body_cta=board['bodyCta'],
			button_cta=board['buttonCta'],
			name=board['name']
		)
		self.board = board
		self.datetime = datetime.strptime(time_created, '%Y-%m-%dT%H:%M:%S.%fZ')
		self.can_edit = can_edit
		self.can_comment = can_comment
		self.can_pin = can_pin
		self.can_set_type = can_set_type
		self.can_report = can_report
		self.has_reported = has_reported
		self.is_locked = is_locked
		self.show_hosted = show_hosted
		self.votes = vote_count
		self.can_vote = can_vote
		self.has_voted = has_voted

		if user is not None:
			user = User(
				client,
				user=user
			)
		self.author = user
		if repl is None:
			self.repl = None
		else:
			self.repl = Repl(
				id=repl['id'],
				embed_url=repl['embedUrl'],
				hosted_url=repl['hostedUrl'],
				title=repl['title'],
				language=repl['language'],
				language_name=repl['languageDisplayName']
			)

	def __repr__(self):
		return f'<{self.title}>'

	def __eq__(self, post2):
		return self.id == post2.id

	def __ne__(self, post2):
		return self.id != post2.id

	async def get_comments(self, order='new'):
		_comments = await self.client._get_comments(
			self.id,
			order
		)
		comments = []
		for c in _comments['comments']['items']:
			comments.append(Comment(
				self.client,
				id=c['id'],
				body=c['body'],
				time_created=c['timeCreated'],
				can_edit=c['canEdit'],
				can_comment=c['canComment'],
				can_report=c['canReport'],
				has_reported=c['hasReported'],
				url=c['url'],
				votes=c['voteCount'],
				can_vote=c['canVote'],
				has_voted=c['hasVoted'],
				user=c['user'],
				post=self,
				comments=c['comments']
			))
		return comments

	async def post_comment(self, content):
		c = await self.client.perform_graphql(
			'createComment',
			graphql.create_comment,
			input={
				'body': content,
				'postId': self.id
			}
		)
		c = c['comment']
		return Comment(
			self,
			id=c['id'],
			body=c['body'],
			time_created=c['timeCreated'],
			can_edit=c['canEdit'],
			can_comment=c['canComment'],
			can_report=c['canReport'],
			has_reported=c['hasReported'],
			url=c['url'],
			votes=c['voteCount'],
			can_vote=c['canVote'],
			has_voted=c['hasVoted'],
			user=c['user'],
			post=self,
			comments=[]
		)


class User():
	def __init__(
		self, client, user
	):
		self.client = client
		self.data = user
		self.id = user['id']
		self.name = user['username']
		self.avatar = user['image']
		self.url = user['url']
		self.cycles = user['karma']
		self.roles = user['roles']

	def __repr__(self):
		return f'<{self.name} ({self.cycles})>'


class Leaderboards():
	def __init__(self, client, limit):
		self.limit = limit
		self.iterated = 0
		self.users = []
		self.raw_users = []
		self.next_cursor = None
		self.client = client

	def __await__(self):
		return self.load_all().__await__()

	def __aiter__(self):
		return self

	def __next__(self):
		raise NotImplementedError

	async def load_all(self):
		async for _ in self: _
		return self.users

	async def __anext__(self):
		ended = len(self.users) + 1 > self.limit
		if self.iterated <= len(self.users) and not ended:
			self.iterated += 30
			leaderboard = await self.client._get_leaderboard(
				self.next_cursor
			)
			self.next_cursor = leaderboard['pageInfo']['nextCursor']
			self.raw_users.extend(leaderboard['items'])

		if ended:
			raise StopAsyncIteration
		user = self.raw_users[len(self.users)]
		user = User(
			self,
			user=user
		)

		self.users.append(user)
		return user

	def __repr__(self):
		if self.iterated >= self.limit:
			return f'<top {self.limit} leaderboard users (cached)>'
		return f'<top {self.limit} leaderboard users>'

	def __str__(self):
		return self.__repr__()


class graphql:
	'There are all the graphql strings used'
	user_part = '''
		user {
			id
			username
			url
			image
			roles
			karma
		}'''
	repl_part = '''
		repl {
			id
			embedUrl: url(lite: true)
			hostedUrl
			title
			language
			languageDisplayName
			timeCreated
		}'''
	board_part = '''
	board {
		id
		url
		slug
		titleCta
		bodyCta
		buttonCta
		description
		name
	}'''
	create_comment = f'''
	mutation createComment($input: CreateCommentInput!) {{
		createComment(input: $input) {{
			comment {{
				id
				...CommentDetailComment
				comments {{
					id
					...CommentDetailComment
				}}
				parentComment {{
					id
				}}
			}}
		}}
	}}

	fragment CommentDetailComment on Comment {{
		id
		body
		timeCreated
		canEdit
		canComment
		canReport
		hasReported
		url
		voteCount
		canVote
		hasVoted
		{user_part}
	}}
	'''
	get_post = f'''
	query post($id: Int!) {{
		post(id: $id) {{
			id
			title
			body
			isAnnouncement
			url
			timeCreated
			canEdit
			canComment
			canPin
			canSetType
			canReport
			hasReported
			isLocked
			showHosted
			voteCount
			canVote
			hasVoted
			{user_part}
			{repl_part}
			{board_part}
		}}
	}}
	'''
	get_leaderboard = '''
	query leaderboard($after: String) {
		leaderboard(after: $after) {
			pageInfo {
				nextCursor
			}
			items {
				id
				username
				image
				url
				karma
				roles
			}
		}
	}
	'''
	get_all_posts = f'''
	query posts($order: String, $after: String, $searchQuery: String) {{
		posts(order: $order, after: $after, searchQuery: $searchQuery) {{
			pageInfo {{
				nextCursor
			}}
			items {{
				id
				title
				body
				timeCreated
				canEdit
				canComment
				canPin
				canSetType
				canReport
				hasReported
				isAnnouncement
				isLocked
				showHosted
				url
				voteCount
				canVote
				hasVoted
				{user_part}
				{repl_part}
				{board_part}
			}}
		}}
	}}
	'''
	post_by_board = f'''
	query postsByBoard(
		$id: Int!, $searchQuery: String, $postsOrder: String, $postsAfter: String
	) {{
		postsByBoard(
			id: $id, searchQuery: $searchQuery, order: $postsOrder, after: $postsAfter
		) {{
			pageInfo {{
				nextCursor
			}}
			items {{
				id
				title
				body
				url
				commentCount
				isPinned
				isLocked
				isAnnouncement
				timeCreated
				voteCount
				canVote
				hasVoted
				{board_part}
				canEdit
				canComment
				canPin
				canSetType
				canReport
				hasReported
				showHosted
				{repl_part}
				{user_part}
			}}
		}}
	}}
	'''
	get_comments = f'''
	query post(
		$id: Int!, $commentsOrder: String, $commentsAfter: String
	) {{
		post(id: $id) {{
			comments(order: $commentsOrder, after: $commentsAfter) {{
				pageInfo {{
					nextCursor
				}}
				items {{
					...CommentDetailComment
					comments {{
						...CommentDetailComment
					}}
				}}
			}}
		}}
	}}

	fragment CommentDetailComment on Comment {{
		id
		body
		timeCreated
		canEdit
		canComment
		canReport
		hasReported
		url
		voteCount
		canVote
		hasVoted
		{user_part}
	}}

	'''
	get_all_comments = f'''
	query comments($after: String, $order: String) {{
		comments(after: $after, order: $order) {{
			items {{
				...CommentDetailComment
				comments {{
					id
					...CommentDetailComment
				}}
			}}
			pageInfo {{
				hasNextPage
				nextCursor
			}}
		}}
	}}


	fragment CommentDetailComment on Comment {{
		id
		body
		timeCreated
		canEdit
		canComment
		canReport
		comments {{
			id
		}}
		hasReported
		url
		voteCount
		canVote
		hasVoted
		...CommentVoteControlComment
		{repl_part}
		post {{
			...PostListItemPost
		}}
	}}

	fragment PostListItemPost on Post {{
		id
		title
		body
		timeCreated
		canEdit
		canComment
		canPin
		canSetType
		canReport
		hasReported
		isAnnouncement
		isLocked
		showHosted
		url
		voteCount
		canVote
		hasVoted
		{board_part}
		{repl_part}
		{user_part}
	}}
	'''
	get_user = '''
	query userByUsername(
		$username: String!,
		$pinnedReplsFirst: Boolean,
		$count: Int,
		$after: String,
		$before: String,
		$direction: String,
		$order: String
	) {
		user: userByUsername(username: $username) {
			id
			username
			firstName
			lastName
			fullName
			displayName
			isLoggedIn
			image
			roles
			karma
			bio
			url
			organization {
				name __typename
			}
			subscription { planId __typename }
			languages { value __typename }
			repls: publicRepls(
				pinnedReplsFirst: $pinnedReplsFirst,
				count: $count,
				after: $after,
				before: $before,
				direction: $direction,
				order: $order) {
					items {
						id
						timeCreated
						pinnedToProfile
						...ProfileReplItemRepl
						__typename
					} pageInfo {
						hasNextPage
						nextCursor
						__typename
					}
					__typename
				} __typename
			}
		}

		fragment ProfileReplItemRepl on Repl {
			id ...ReplItemBaseRepl __typename
		}

		fragment ReplItemBaseRepl on Repl {
			id url title languageDisplayName timeCreated __typename
		}
	'''
	post_exists = 'query post($id: Int!) { post(id: $id) { id } }'


class Client():
	def __init__(self):
		self.default_ref = base_url + '/@mat1/repl-talk-api'
		self.sid = None
		self.boards = self._boards(self)

	async def perform_graphql(self, operation_name, query, **variables):
		payload = {
			'operationName': operation_name,
			'variables': variables,
			'query': query
		}

		async with aiohttp.ClientSession(
			cookies={'connect.sid': self.sid},
			headers={'referer': self.default_ref}
		) as s:
			async with s.post(
				base_url + '/graphql',
				json=payload
			) as r:
				data = await r.json()
		if 'data' in data:
			data = data['data']
		if data is None:
			return None
		keys = data.keys()
		if len(keys) == 1:
			data = data[next(iter(keys))]
		return data

	async def login(self, username, password):
		if username.lower() not in whitelisted_bots:
			raise NotWhitelisted(
				f'{username} is not whitelisted and therefore is not allowed to log in.\n'
				'Please ask mat#6207 if you would like to be added to the whitelist.'
			)

		async with aiohttp.ClientSession(
			headers={'referer': self.default_ref}
		) as s:
			async with s.post(
				base_url + '/login',
				json={
					'username': username,
					'password': password,
					'teacher': False
				}
			) as r:
				if await r.text() == '{"message":"Invalid username or password."}':
					raise InvalidLogin('Invalid username or password.')
				# Gets the connect.sid cookie
				connectsid = str(dict(r.cookies)['connect.sid'].value)
				self.sid = connectsid
			return self

	async def _get_post(self, post_id):
		post = await self.perform_graphql(
			'post', graphql.get_post, id=post_id
		)
		return post

	async def get_post(self, post_id):
		post = await self._get_post(post_id)
		return Post(
			self,
			id=post['id'],
			title=post['title'],
			body=post['body'],
			is_announcement=post['isAnnouncement'],
			url=post['url'],
			board=post['board'],
			time_created=post['timeCreated'],
			can_edit=post['canEdit'],
			can_comment=post['canComment'],
			can_pin=post['canPin'],
			can_set_type=post['canSetType'],
			can_report=post['canReport'],
			has_reported=post['hasReported'],
			is_locked=post['isLocked'],
			show_hosted=post['showHosted'],
			vote_count=post['voteCount'],
			can_vote=post['canVote'],
			has_voted=post['hasVoted'],
			user=post['user'],
			repl=post['repl']
		)

	async def post_exists(self, post_id):
		if isinstance(post_id, Post):
			post_id = post_id.id
		post = await self.perform_graphql(
			'post', graphql.post_exists, id=post_id
		)
		return post is not None

	async def _get_leaderboard(self, cursor=None):
		if cursor is None:
			leaderboard = await self.perform_graphql(
				'leaderboard',
				graphql.get_leaderboard
			)
		else:
			leaderboard = await self.perform_graphql(
				'leaderboard',
				graphql.get_leaderboard,
				after=cursor
			)
		return leaderboard

	def get_leaderboard(self, limit=30):
		return Leaderboards(self, limit)

	async def _get_all_posts(
		self, order='new', search_query='', after=None
	):
		if after is None:
			posts = await self.perform_graphql(
				'posts',
				graphql.get_all_posts,
				order=order,
				searchQuery=search_query
			)
			return posts
		else:
			posts = await self.perform_graphql(
				'posts',
				graphql.get_all_posts,
				order=order,
				searchQuery=search_query,
				after=after
			)
			return posts

	async def _posts_in_board(
		self, order='new', search_query='', board_id=0, after=None
	):
		if board_id == 0:
			raise Exception('board id cant be 0')
		if after is None:
			posts = await self.perform_graphql(
				'postsByBoard',
				graphql.post_by_board,
				postsOrder=order,
				searchQuery=search_query,
				id=board_id
			)
			return posts
		else:
			posts = await self.perform_graphql(
				'postsByBoard',
				graphql.post_by_board,
				postsOrder=order,
				searchQuery=search_query,
				postsAfter=after,
				id=board_id
			)
			return posts

	class _boards:
		for board in ('All', 'Announcements', 'Challenge', 'Ask', 'Learn', 'Share'):
			board_name = '_' + board.lower()
			locals()[board_name] = type(
				board_name,
				(Board,),
				{'name': board}
			)
			# Creates classes for each of the boards
		del board	 # Don't want that extra class var

		def __init__(self, client):
			self.client = client

			self.all = self._all(client)
			self.announcements = self._announcements(client)
			self.challenge = self._challenge(client)
			self.ask = self._ask(client)
			self.learn = self._learn(client)
			self.share = self._share(client)

	async def _get_comments(self, post_id, order='new'):
		return await self.perform_graphql(
			'post',
			graphql.get_comments,
			id=post_id,
			commentsOrder=order
		)

	async def _get_all_comments(self, order='new'):
		return await self.perform_graphql(
			'comments',
			graphql.get_all_comments,
			order=order
		)

	async def get_all_comments(self, order='new'):
		_comments = await self._get_all_comments(order=order)
		comments = []
		for c in _comments['items']:
			comments.append(Comment(
				self,
				id=c['id'],
				body=c['body'],
				time_created=c['timeCreated'],
				can_edit=c['canEdit'],
				can_comment=c['canComment'],
				can_report=c['canReport'],
				has_reported=c['hasReported'],
				url=c['url'],
				votes=c['voteCount'],
				can_vote=c['canVote'],
				has_voted=c['hasVoted'],
				user=c['user'],
				post=c['post'],
				comments=c['comments']
			))
		return comments

	async def _get_user(self, name):
		user = await self.perform_graphql(
			'userByUsername',
			graphql.get_user,
			username=name,
		)
		return user

	async def get_user(self, name):
		user = await self._get_user(name)
		if user is None:
			return None
		u = User(
			self,
			user=user
		)
		return u
