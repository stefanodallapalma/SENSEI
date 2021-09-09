import React, { Component,useEffect, useState } from 'react';
import axios from 'axios';
import Grid from '@material-ui/core/Grid';

import CircularProgress from '@material-ui/core/CircularProgress';
import MaterialTable from 'material-table';
import Slide from '@material-ui/core/Slide';


const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

  
  function ReviewTable() {
    // Set useStates
    const [value, setValue] = useState(0);
    const [data, setData] = useState([]);
    const [open, setOpen] = useState(false);
    const [loaded, setLoaded] = useState(false);

    // Load data
    useEffect( async() => {
        const all_data = await axios.get("http://" + process.env.REACT_APP_BACKEND_HOST + ":" + process.env.REACT_APP_BACKEND_PORT + "/rawdata");
        setData(all_data.data[1]);
        setLoaded(true);
    }, [])
  
  
    // Define column names. 'field' should be equal to the naming within the loaded data
    const columns = [
    {title:"Vendor reviewed", field:"name"},
    {title: 'Market', field:'market'},
    {title: 'Message', field:'message'},
    {title: 'Product bought', field:'product'},
    {title: "Timestamp review", field:'timestamp'}
    ]
  


    const handleChange = (event, newValue) => {
      setValue(newValue);
      };

    if (loaded) {
      // Define what has to be in the rows (which is the loaded data)
        const rows = data;

    return (
      <Grid
          container
          direction="column"
          justify="center"
          alignItems="center"
        >
        <div className="table" style={{width: '85%'}}>
         <br></br>
          
       <MaterialTable title="Reviews table"
       data = {rows}
       columns={columns}
       options={{
         filtering:true,
         exportButton:true,
         pageSize:12,
         headerStyle: {
          fontWeight: 'bold',
          color: '#000000'
      }}} 
      
         
       />

    
      </div>
      </Grid>
        
    );
  } else {

    return (
        <Grid
          container
          spacing={0}
          direction="column"
          alignItems="center"
          justify="center"
          style={{ minHeight: '100vh' }}
        >

          <Grid item xs={3}>
            <CircularProgress />
          </Grid>   

    </Grid>  
      );
  }


}

export default ReviewTable;


