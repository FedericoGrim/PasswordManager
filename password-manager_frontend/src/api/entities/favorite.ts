export class favorite {
    id: string;
    user_id: string;
    sub_account_id: string;

    constructor(fields: { id: string; user_id: string; sub_account_id: string }) {
        this.id = fields.id;
        this.user_id = fields.user_id;
        this.sub_account_id = fields.sub_account_id;
    }
}
