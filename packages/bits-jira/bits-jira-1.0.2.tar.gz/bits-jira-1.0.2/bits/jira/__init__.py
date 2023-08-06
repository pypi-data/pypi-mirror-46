"""Jira class file."""

from jira.client import JIRA


class Jira(object):
    """Jira class."""

    def __init__(
        self,
        username,
        password,
        server='https://company.atlassian.net',
        verbose=False,
    ):
        """Initialize a JIRA class instance."""
        self.jira = None

        self.jira_server = server
        self.jira_username = username
        self.jira_password = password

        self.verbose = verbose

        if username and password:
            self.connect()

    def connect(self):
        """Connect to JIRA."""
        self.jira = JIRA(
            basic_auth=(self.jira_username, self.jira_password),
            server=self.jira_server,
        )

    #
    # Groups
    #
    def get_group_members(self, group):
        """Return a list of members in a group."""
        if not self.jira:
            self.connect()
        return self.jira.group_members(group)

    def get_groups(self):
        """Return a list of JIRA Group names."""
        if not self.jira:
            self.connect()
        return self.jira.groups()

    def get_groups_with_members(self):
        """Return na list of JIRA Groups."""
        group_names = self.get_groups()
        groups = []
        for name in group_names:
            print(name.raw)
            members = self.jira.group_members(name)
            groups.append({'id': name, 'members': members})
        return groups

    def get_members_to_add(self, current, members):
        """Return a list of members to add to a group."""
        add = []
        for m in members:
            if m not in current:
                add.append(m)
        return add

    def get_members_to_remove(self, current, members):
        """Return a list of members to remove from a group."""
        remove = []
        for m in current:
            if m not in members:
                remove.append(m)
        return remove

    def update_group_members(self, group, members):
        """Update the members of a group to match provided members list."""
        current = self.get_group_members(group)

        add = self.get_members_to_add(current, members)
        remove = self.get_members_to_remove(current, members)

        if add:
            print('    Adding members:')
            for m in sorted(add):
                error = ''
                try:
                    self.jira.add_user_to_group(m, group)
                except Exception as e:
                    error = ' (%s)' % (e.text)
                print('     + %s%s' % (m, error))

        if remove:
            print('    Removing members:')
            for m in sorted(remove):
                error = ''
                try:
                    self.jira.remove_user_from_group(m, group)
                except Exception as e:
                    error = ' (%s)' % (e.text)
                print('     - %s%s' % (m, error))

    #
    # Projects
    #
    def get_projects(self):
        """Return a list of JIRA Group projects."""
        if not self.jira:
            self.connect()
        return self.jira.projects()

    def get_projects_dict(self):
        """Return a dict of JIRA Group projects."""
        projects = {}
        for p in self.get_projects():
            projects[p.key] = p.raw
        return projects

    #
    # Users
    #
    def get_users(
        self,
        query='',
        startAt=0,
        maxResults=1000,
        includeActive=True,
        includeInactive=True,
    ):
        """Return a list of all users."""
        # connect to jira
        if not self.jira:
            self.connect()

        all_users = []

        # get first page of user results
        users = self.get_users_page(
            query,
            startAt,
            maxResults,
            includeActive,
            includeInactive
        )
        all_users.extend(users)

        # get additional pages of user results
        while len(users) == maxResults:
            startAt = len(all_users)
            users = self.get_users_page(
                query,
                startAt,
                maxResults,
                includeActive,
                includeInactive
            )
            all_users.extend(users)
        return all_users

    def get_users_dict(
        self,
        query='',
        startAt=0,
        maxResults=1000,
        includeActive=True,
        includeInactive=True,
    ):
        """Return a list of all users."""
        all_users = self.get_users(
            query,
            startAt,
            maxResults,
            includeActive,
            includeInactive
        )

        # convert to dict
        users = {}
        for u in all_users:
            email = u['emailAddress']
            users[email] = u
        return users

    def get_users_page(
        self,
        query='',
        startAt=0,
        maxResults=1000,
        includeActive=True,
        includeInactive=False,
    ):
        """Return a single page of user results."""
        if self.verbose:
            print('Retrieving %s results for query: "%s" starting at %s' % (
                maxResults,
                query,
                startAt,
            ))
        results = self.jira.search_users(
            query,
            startAt,
            maxResults,
            includeActive,
            includeInactive,
        )
        users = []
        for u in results:
            users.append(u.raw)
        if self.verbose:
            print('Retrieved %s users' % (len(users)))
        return users

    def process_users_export_csv(self, lines):
        """Return a list of users from a users-export.csv."""
        users = []

        for u in lines:
            # display name
            u['displayName'] = u['full_name']
            del u['full_name']

            # email
            u['emailAddress'] = u['email']
            del u['email']

            # active
            if u['active'] == 'Yes':
                u['active'] = True
            elif u['active'] == 'No':
                u['active'] = False

            users.append(u)

        return users
