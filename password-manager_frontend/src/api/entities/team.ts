export class team {
    id: string;
    name: string;
    is_personal: boolean;

    constructor(fields: { id: string; name: string; is_personal: boolean }) {
        this.id = fields.id;
        this.name = fields.name;
        this.is_personal = fields.is_personal;
    }
}
