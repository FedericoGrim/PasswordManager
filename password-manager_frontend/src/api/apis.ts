import axiosClient from './axiosClient';
import axios from 'axios';
import { mainUser } from './entities/mainUser';
import { subAccount } from './entities/subAccount';
import { UUID } from 'crypto';

axiosClient.defaults.headers.common['Content-Type'] = 'application/json';

const createMainUser = async (): Promise<void> => {
    try {
        await axiosClient.post('/api/user/'); 
    } catch (error) {
        console.error('Error creating main user:', error);
        throw error;
    }
}

const getMainUserMe = async (): Promise<mainUser | null> => {
    try {
        const response = await axiosClient.get('/api/user/me');
        return response.data.user as mainUser;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response?.status === 404) {
            return null;
        }
        console.error('Error fetching user data:', error);
        throw error;
    }
};

const updateMainUser = async (user: mainUser): Promise<void> => {
    try {
        await axiosClient.put(`/api/localuser/${user.Id}`, user);
    } catch (error) {
        console.error('Error updating main user:', error);
        throw error;
    }
};

const deleteMainUser = async (id: UUID): Promise<void> => {
    try {
        await axiosClient.delete(`/api/localuser/${id}`);
    } catch (error) {
        console.error('Error deleting main user:', error);
        throw error;
    }
};

const createSubAccount = async (UserId: string, SubAccount: subAccount): Promise<void> => {
    try {
        await axiosClient.post(
            `/api/subaccount/${UserId}`,
            {
                user_id: UserId,
                title: SubAccount.title,
                username: SubAccount.username,
                password: SubAccount.password,
                url: SubAccount.url
            }
        );
    } catch (error) {
        console.error('Error creating sub account:', error);
        throw error;
    }
}

const getMySubAccounts = async (): Promise<subAccount[]> => {
  try {
    const response = await axiosClient.get('/api/subaccount/');
    return response.data.subaccounts as subAccount[];
  } catch (error) {
    console.error("Error fetching sub accounts:", error);
    return [];
  }
};

const updateSubAccount = async (subaccount : subAccount, subaccount_id: UUID): Promise<void> => {
    try {
        await axiosClient.put(
            `/api/subaccount/${subaccount_id}`,
            {
                title: subaccount.title ?? "",
                username: subaccount.username ?? "",
                password: subaccount.password ?? "",
                url: subaccount.url ?? ""
            }
        );
    } catch (error) {
        console.error("Error updating sub account:", error);
        throw error;
    }
};

const deleteSubAccount = async (subaccount_id: UUID): Promise<void> => {
    console.log("Deleting sub account:", { subaccount_id });
    try {
        await axiosClient.delete(`/api/subaccount/${subaccount_id}`);
    } catch (error) {
        console.error("Error deleting sub account:", error);
        throw error;
    }
};


export {
    createMainUser,
    getMainUserMe,
    updateMainUser,
    deleteMainUser,
    createSubAccount,
    getMySubAccounts,
    updateSubAccount,
    deleteSubAccount
};