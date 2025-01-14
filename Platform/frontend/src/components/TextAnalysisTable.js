import React, { Component,useEffect, useState } from 'react';
import axios from 'axios';
import Grid from '@material-ui/core/Grid';
import CircularProgress from '@material-ui/core/CircularProgress';
import MaterialTable from 'material-table';
import Typography from '@material-ui/core/Typography';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import Slide from '@material-ui/core/Slide';
import Button from '@material-ui/core/Button';




const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

  
  function TextAnalysisTable() {

  
  // Set Usestates
    const [value, setValue] = useState(0);
    const [data, setData] = useState([]);
    const [open, setOpen] = useState(false);
    const [vendorInfo, setVendorInfo] = useState()
    const [vendorName, setVendorName] = useState()
    const [vendorPGP, setVendorPGP] = useState()
    const [loaded, setLoaded] = useState(false);

    useEffect( async() => {
        const all_data = await axios.get("http://" + process.env.REACT_APP_BACKEND_HOST + ":" + process.env.REACT_APP_BACKEND_PORT + "/operational");
        setData(all_data.data[0]);
        setLoaded(true);
    }, [])
  
  
  // Define column names. 'field' should be equal to the naming within the loaded data
    const columns = [
      {title: 'Timestamp', field:'timestamp'},
      {title:"Market", field:"market"},
      {title: 'Name', field:'name'},
      {title: "E-mail", field:'email'},
      {title: "Phone number", field:"phone number"},
      {title:"Wickr id", field:"wickr"},
      {title: 'Other markets', field:'other markets'},
      {title: 'Group or individual', field:'group/individual'},
      {title:"Info", field:"info"}
    ]
  

    const handleClickOpen = () => {
      setOpen(true);
    };
  
    const handleClose = () => {
      setOpen(false);
    };

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
          
       <MaterialTable title="Vendor table"
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
      onRowClick={(event, rowData, togglePanel) => {setVendorInfo(rowData['info']); setVendorPGP(rowData['pgp']); setVendorName(rowData['name']); handleClickOpen()}}
         
       />

      <Dialog
            open={open}
            maxWidth="sm"
            TransitionComponent={Transition}
            keepMounted
            onClose={handleClose}
            aria-labelledby="alert-dialog-slide-title"
            aria-describedby="alert-dialog-slide-description"
          >
            <DialogTitle id="alert-dialog-slide-title">{vendorName}</DialogTitle>
            <DialogContent>
              <DialogContentText id="alert-dialog-slide-description">
              <Typography variant="body2">
              {vendorInfo}
              </Typography>
                
              </DialogContentText>
            </DialogContent>
            <DialogActions>
              <Button onClick={handleClose} color="primary">
                Close
              </Button>
            </DialogActions>
          </Dialog>
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

export default TextAnalysisTable;


