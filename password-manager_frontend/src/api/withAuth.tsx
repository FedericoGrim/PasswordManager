import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { keycloakFactory, hasRoleAccess } from './keycloakClient';

const withAuth = (Component: React.ComponentType, requiredRole: string) => {
  const AuthenticatedComponent = (props: any) => {
    const router = useRouter();
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);

    useEffect(() => {
      const keycloak = keycloakFactory();

      const checkAuth = () => {
        const hasAccess = hasRoleAccess(requiredRole);
        setIsAuthenticated(hasAccess);
        if (!hasAccess) {
          router.push('/not-authorized');
        }
      };

      if (keycloak.authenticated) {
        checkAuth();
      } else {
        keycloak.onAuthSuccess = checkAuth;
        keycloak.onAuthError = () => router.push('/not-authorized');
      }
    }, [router]);

    if (isAuthenticated === false) {
      return <div>Loading...</div>; 
    }

    if (isAuthenticated) {
      return <Component {...props} />;
    }

    return null; 
  };

  AuthenticatedComponent.displayName = `withAuth(${Component.displayName || Component.name || 'Component'})`;

  return AuthenticatedComponent;
};

export default withAuth;
