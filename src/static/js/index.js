let datatable;
let dataTableIsInitialized = false;

const options = {
    columnsDefs:[
        {className:'centered', targets:[0,1,2,3,4]},
        {orderrable: false, target:[4]},
        {searchable: false, targets:[0,1,2,3,4]}
    ],
    pageLength:4,
    destroy:true
    
}

const initDataTable = async () =>{
    if(dataTableIsInitialized){
        datatable.destroy();
    }
    await listProducts();
    dataTable = $('#datatable_products').DataTable({});
    dataTableIsInitialized = true;
}

const listProducts = async() =>{
    try{
        const response = await fetch('http://127.0.0.1:5000/list_products');
        const data = await response.json();
        let content =``;
        data.products.forEach((product,index) =>{
            content+=`
            <tr>
                <td>${product.sku}</td>
                <td>${product.name}</td>
                <td>${product.price}</td>
                <td>${product.brand}</td>
            </tr>
            `;
        })
        $('#datatable_products tbody').html(content); // Actualizar el contenido de la tabla
        console.log(data);
    }catch(error){
        console.log('error:',error);
    }
}

window.addEventListener('load',async()=>{
    await initDataTable();
});