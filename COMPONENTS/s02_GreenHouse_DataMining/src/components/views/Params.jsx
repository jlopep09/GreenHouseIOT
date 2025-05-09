import Navbar from '../overlay/Navbar';
import Devicebar from '../overlay/Devicebar';
import Sidebar from '../overlay/Sidebar';
import Donut from '../charts/Donut';
import Barchart from '../charts/Barchart';
import Linechart from '../charts/Linechart';


export default function Params() {
    
    return (
        <>
            <div className="drawer">
                <input id="my-drawer" type="checkbox" className="drawer-toggle" />
                <div className="drawer-content flex grow flex-col overflow-hidden pb-4">
                    {/* Page content here */}
                    <Navbar/>
                    <Devicebar/>
                    <section className='card flex flex-row gap-4 justify-center my-3'>
                        <div className='card bg-base-200'>
                            <Linechart chartWidth={600}></Linechart>
                        </div>
                        <div className='card bg-base-200'>
                            <Linechart metric="water_temperature" chartWidth={600} />
                        </div>
                        
                        
                    </section>
                    <section className='card flex flex-row gap-4 justify-center my-3'>
                        <div className='card bg-base-200'>
                            <Linechart metric="humidity" chartWidth={600} />
                        </div>
                        <div className='card bg-base-200'>
                            <Linechart metric="tds" chartWidth={600} />
                        </div>
                        
                        
                        
                    </section>
                    {/**
                     * <section className='card bg-base-200 flex flex-row gap-4 justify-center'>
                        <Donut></Donut>
                        <Barchart></Barchart>
                    </section>
                     * 
                     * 
                     * 
                     */}

                </div>
                <Sidebar/>
            </div>
        </>
    );
}

