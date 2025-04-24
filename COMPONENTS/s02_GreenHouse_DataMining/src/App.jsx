import {useEffect, useState} from 'react';
import Navbar from './components/overlay/Navbar';
import Sidebar from './components/overlay/Sidebar';
import Devicebar from './components/overlay/Devicebar';
import { Content } from './components/overlay/Content';
import { useAuth0 } from "@auth0/auth0-react";

export default function App() {
    const {
        user,
        isAuthenticated,
        isLoading,
        getAccessTokenSilently,
      } = useAuth0();
    useEffect(() => {
        const ensureUserInDb = async () => {
            if (!isAuthenticated || !user) return;

            try {
            // 1) Obtener el token de usuario
            const token = await getAccessTokenSilently();

            // 2) Llamar a tu endpoint de creación/comprobación de usuario
            await fetch(`${import.meta.env.VITE_DDBB_API_IP}/db/users/`, {
                method: "POST",
                headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${import.meta.env.VITE_SECRET_TOKEN}`,   // tu token de API
                "UserAuth": token,                                                // token de Auth0
                },
                body: JSON.stringify({
                auth0_id: user.sub,
                email: user.email,
                name: user.name
                }),
            });
            } catch (e) {
            console.error("Error asegurando usuario en BBDD:", e);
            }
        };

        ensureUserInDb();
    }, [isAuthenticated, user, getAccessTokenSilently]);
    if (isLoading) return <div>Loading…</div>;
    return (
        <>
            {!isAuthenticated && <LoginButton />}
            {isAuthenticated && (
                <div className="drawer">
                    <input id="my-drawer" type="checkbox" className="drawer-toggle" />
                    <div className="drawer-content flex grow flex-col max-h-lvh overflow-hidden">
                        {/* Page content here */}
                        <Navbar/>
                        <Devicebar/>
                        <Content/>
                    </div>
                    <Sidebar/>
                </div>
            )}
        </>
    );
}
