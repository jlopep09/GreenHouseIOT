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
                <div className="drawer-content flex grow flex-col max-h-lvh overflow-hidden">
                    {/* Page content here */}
                    <Navbar/>
                    <Devicebar/>
                    <section className='card bg-base-200 flex flex-row gap-4 justify-center'>
                        <Donut></Donut>
                        <Barchart></Barchart>
                        <Linechart></Linechart>
                    </section>

                </div>
                <Sidebar/>
            </div>
        </>
    );
}

