export class userTeamsKey {
    id: string;
    user_id: string;
    team_id: string;
    team_key_encrypted: string;

    constructor(fields: { id: string; user_id: string; team_id: string; team_key_encrypted: string }) {
        this.id = fields.id;
        this.user_id = fields.user_id;
        this.team_id = fields.team_id;
        this.team_key_encrypted = fields.team_key_encrypted;
    }
}
