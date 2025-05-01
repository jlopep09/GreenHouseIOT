import React, { useState } from 'react';

export default function AddNewGH({children}) {
    const [isOpen, setIsOpen] = useState(false);

    const handleSubmit = (event) => {
        event.preventDefault();
        alert('Se ha enviado correctamente');
        setIsOpen(false);
    };

    return (
        <>
            <button className="btn btn-primary" onClick={() => setIsOpen(true)}>
                {children}
            </button>

            {isOpen && (
                <dialog className="modal modal-open">
                    <div className="modal-box">
                        <h3 className="font-bold text-lg">Nueva configuración</h3>
                        <form onSubmit={handleSubmit} className="flex flex-col gap-4 mt-4">
                            <input type="text" placeholder="Nombre" className="input input-bordered w-full" required />
                            <input type="text" placeholder="Ip 192.168.1.201" className="input input-bordered w-full" required />
                            <input type="text" placeholder="Ip cámara: 192.168.1.202" className="input input-bordered w-full" required />
                            <textarea placeholder="Descripción" className="textarea textarea-bordered w-full"></textarea>
                            <div className="flex justify-end gap-2">
                                <button type="button" className="btn" onClick={() => setIsOpen(false)}>
                                    Cancelar
                                </button>
                                <button type="submit" className="btn btn-primary">Enviar</button>
                            </div>
                        </form>
                    </div>
                </dialog>
            )}
        </>
    );
}