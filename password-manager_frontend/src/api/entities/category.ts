export class category {
    id: string;
    team_id: string;
    name: string;

    constructor(fields: { id: string; team_id: string; name: string }) {
        this.id = fields.id;
        this.team_id = fields.team_id;
        this.name = fields.name;
    }
}
