import axiosClient from './axiosClient';
import { keycloakFactory } from './keycloakClient';
import { mainUser } from './entities/mainUser';
import { subAccount } from './entities/subAccount';
import { UUID } from 'crypto';

axiosClient.defaults.headers.common['Content-Type'] = 'application/json';

const createMainUser = async (user: mainUser): Promise<void> => {
    try {
        await axiosClient.post('/mainUser', user);
    } catch (error) {
        console.error('Error creating main user:', error);
        throw error;
    }
}

const getMainUserByKeycloakId = async (keycloak_user_id: UUID): Promise<mainUser | null> => {
    try {
        const response = await axiosClient.get(`/api/V1/localuser/${keycloak_user_id}`);
        return response.data.user as mainUser;
    } catch (error) {
        console.error('Error fetching main user:', error);
        return null;
    }
};

const updateMainUser = async (user: mainUser): Promise<void> => {
    try {
        await axiosClient.put(`/api/V1/localuser/${user.Id}`, user);
    } catch (error) {
        console.error('Error updating main user:', error);
        throw error;
    }
};

const deleteMainUser = async (id: UUID): Promise<void> => {
    try {
        await axiosClient.delete(`/api/V1/localuser/${id}`);
    } catch (error) {
        console.error('Error deleting main user:', error);
        throw error;
    }
};

const createSubAccount = async (UserId: string, SubAccount: subAccount, Salt: string, MasterPassword: string): Promise<void> => {
    try {
        await axiosClient.post(
            `/api/V1/subaccount/${UserId}?salt=${Salt}&master_password=${MasterPassword}`,
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


const getSubAccountsByUserId = async (userId: UUID): Promise<subAccount[]> => {
  try {
    const response = await axiosClient.get(`/api/V1/subaccount/${userId}`, {
      params: { userId }
    });
    console.log(response.data);
    return response.data.subaccounts as subAccount[];
  } catch (error) {
    console.error("Error fetching sub accounts:", error);
    return [];
  }
};

const updateSubAccount = async (subaccount : subAccount, subaccount_id: UUID, salt: string): Promise<void> => {
    try {
        await axiosClient.put(
            `/api/V1/subaccount/${subaccount_id}`,
            {
                title: subaccount.title ?? "",
                username: subaccount.username ?? "",
                password: subaccount.password ?? "",
                url: subaccount.url ?? ""
            },
            {
                params: { salt: salt }
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
        await axiosClient.delete(`/api/V1/subaccount/${subaccount_id}`);
    } catch (error) {
        console.error("Error deleting sub account:", error);
        throw error;
    }
};


export {
    createMainUser,
    getMainUserByKeycloakId,
    updateMainUser,
    deleteMainUser,
    createSubAccount,
    getSubAccountsByUserId,
    updateSubAccount,
    deleteSubAccount
};