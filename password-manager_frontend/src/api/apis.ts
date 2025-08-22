import axiosClient from './axiosClient';
import { keycloakFactory } from './keycloakClient';
import { mainUser } from './entities/mainUser';
import { subAccount } from './entities/subAccount';

axiosClient.defaults.headers.common['Content-Type'] = 'application/json';

const createMainUser = async (user: mainUser): Promise<void> => {
    try {
        await axiosClient.post('/mainUser', user);
    } catch (error) {
        console.error('Error creating main user:', error);
        throw error;
    }
}

const getMainUserByKeycloakId = async (id: string): Promise<mainUser | null> => {
    try {
        const response = await axiosClient.get(`/api/V1/localuser/${keycloak_user_id}`);
        return response.data as mainUser;
    } catch (error) {
        console.error('Error fetching main user:', error);
        return null;
    }
};

const updateMainUser = async (user: mainUser): Promise<void> => {
    try {
        await axiosClient.put(`/mainUser/${user.Id}`, user);
    } catch (error) {
        console.error('Error updating main user:', error);
        throw error;
    }
};

const deleteMainUser = async (id: string): Promise<void> => {
    try {
        await axiosClient.delete(`/mainUser/${id}`);
    } catch (error) {
        console.error('Error deleting main user:', error);
        throw error;
    }
};

const createSubAccount = async (subAccount: subAccount): Promise<void> => {
    try {
        await axiosClient.post('/subAccount', subAccount);
    } catch (error) {
        console.error('Error creating sub account:', error);
        throw error;
    }
}

const getSubAccountsByUserId = async (userId: string): Promise<subAccount[]> => {
    try {
        const response = await axiosClient.get(`/subAccount`, { params: { userId } });
        return response.data as subAccount[];
    } catch (error) {
        console.error('Error fetching sub accounts:', error);
        return [];
    }
};

const updateSubAccount = async (subAccount: subAccount): Promise<void> => {
    try {
        await axiosClient.put(`/subAccount/${subAccount.Id}`, subAccount);
    } catch (error) {
        console.error('Error updating sub account:', error);
        throw error;
    }
};

const deleteSubAccount = async (id: string): Promise<void> => {
    try {
        await axiosClient.delete(`/subAccount/${id}`);
    } catch (error) {
        console.error('Error deleting sub account:', error);
        throw error;
    }
};

export {
    createMainUser,
    getMainUserById,
    updateMainUser,
    deleteMainUser,
    createSubAccount,
    getSubAccountsByUserId,
    updateSubAccount,
    deleteSubAccount
};