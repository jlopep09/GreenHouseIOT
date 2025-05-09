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
                <div className="drawer-content flex grow flex-col overflow-hidden gap-3 my-4">
                    {/* Page content here */}
                    <Navbar/>
                    <Devicebar/>
                    <section className='card bg-base-200 flex flex-row gap-4 justify-center'>
                        <Linechart chartWidth={600}></Linechart>
                        <Linechart metric="water_temperature" chartWidth={600} />
                        
                    </section>
                    <section className='card bg-base-200 flex flex-row gap-4 justify-center'>
                        <Linechart metric="humidity" chartWidth={600} />
                        <Linechart metric="tds" chartWidth={600} />
                        
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

