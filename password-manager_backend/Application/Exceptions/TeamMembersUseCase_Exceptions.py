class TeamMemberAdditionException(Exception):
    def __init__(self, message="Error adding member to team"):
        self.message = message
        super().__init__(self.message)

class TeamMembersRetrievalByTeamIdException(Exception):
    def __init__(self, message="Error retrieving team members by Team ID"):
        self.message = message
        super().__init__(self.message)

class TeamsRetrievalByMemberIdException(Exception):
    def __init__(self, message="Error retrieving teams by Member ID"):
        self.message = message
        super().__init__(self.message)

class TeamMemberRoleUpdateException(Exception):
    def __init__(self, message="Error updating team member role"):
        self.message = message
        super().__init__(self.message)

class TeamMemberRemovalException(Exception):
    def __init__(self, message="Error removing member from team"):
        self.message = message
        super().__init__(self.message)