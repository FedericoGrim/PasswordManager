export class teamMember {
    id: string;
    user_id: string;
    team_id: string;
    perm_level_id: string;

    constructor(fields: { id: string; user_id: string; team_id: string; perm_level_id: string }) {
        this.id = fields.id;
        this.user_id = fields.user_id;
        this.team_id = fields.team_id;
        this.perm_level_id = fields.perm_level_id;
    }
}
