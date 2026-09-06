export class teamPermLevel {
    id: string;
    team_id: string;
    name: string;
    rank: number;

    constructor(fields: { id: string; team_id: string; name: string; rank: number }) {
        this.id = fields.id;
        this.team_id = fields.team_id;
        this.name = fields.name;
        this.rank = fields.rank;
    }
}
