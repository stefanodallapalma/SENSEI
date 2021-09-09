import React, { Component,useEffect, useState } from 'react';
import Paper from '@material-ui/core/Paper';
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
import Tour from 'reactour'
import { useLocation } from 'react-router-dom';
import InfoOutlinedIcon from '@material-ui/icons/InfoOutlined';
import Box from '@material-ui/core/Box';
import { useHistory,Link  } from 'react-router-dom';


const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

  
  function ProductTable() {

    
    // Set useStates
    const [value, setValue] = useState(0);
    const [data, setData] = useState([]);
    const [productInfo, setProductInfo] = useState()
    const [open, setOpen] = useState(false);
    const [loaded, setLoaded] = useState(false);
    const [isTourOpen, setIsTourOpen] = useState(false);

    useEffect( async() => {
        const all_data = await axios.get("http://" + process.env.REACT_APP_BACKEND_HOST + ":" + process.env.REACT_APP_BACKEND_PORT + "/rawdata");
        setData(all_data.data[0]);
        setLoaded(true);
    }, [])

    const location = useLocation();
    const history = useHistory();
  
     // This function is used to make sure that the tour functionality can be used
    // Once the page loads, it detects whether anything is present in the location.state
    // If that is the case, the tour is set to true
    // It will be called further on in the script
    function runIt(){
          if (location.state !== undefined){
            console.log(location.state[0])
              if ( location.state[0] === true){
                setIsTourOpen(true)
                  location.state = '';
                  return(null)
               }
          } 
          }

          // These are all the steps of the tour. All of them have to be defined here to make sure that the dots corresponding
        // to the amount of steps left are correct
          const steps = [
           
            {
              content: 'This is my first Step',
              action: () => history.push({pathname: '/overview',state: [true]})
              
            },
            {
              content: <Typography variant="subtitle1">
                Welcome to the Anita dashboard! This tour will tell you all you need to know to get going.
              </Typography>
            },
            {
              content: <div><Typography variant="subtitle1">
              This dashboard aims to make you more knowledgable regarding drug trafficking that takes place on the dark web.
              It is focussed on people that sell drugs, so called vendors. 
            </Typography>
            <Typography variant="subtitle1">
             It contains data, information and intelligence 
          </Typography>
          </div>
            },
            {
              selector:'.data',
              content: <Typography variant="subtitle1">
                The 'raw data' tab allows you to study all the data that has been used throughout the dashboard. Data can be considered
                as the unaltered observations made on the dark web. After this data was collected, personal data 
                was deleted and the aliases of users were pseudonimized.
              </Typography>
            },
            {
              content: 'This is my first Step',
              action: () => history.push({pathname: '/producttable',state: [true]})
              
            },
            {
              selector:'.producttable',
              content: <Typography variant="subtitle1">
                The tables allow you to sort and search for specific words.
              </Typography>
            },
            {
              content: <Typography variant="subtitle1">
                Information can be perceived as a usefull combination of data that increases its value.
                The information sections have been divided by means of the 5 W's central to an investigation.
              </Typography>
            },
            {
              selector:'.operational',
              content: <Typography variant="subtitle1">
                Operational information refers to the "Who" question, therefore allowing you to identify interesting vendors.
              </Typography>
            },
            {
              action: () => history.push({pathname: '/operational',state: [true]})
              
            },
            {
                selector:'.select',
                content: <Typography variant="subtitle1">
                  These selectors allow you to filter out vendors of your interest
                </Typography>
              },
              {
                selector:'.go',
                content: <Typography variant="subtitle1">
                  After clicking go, you will be presented with the vendors, sorted by estimated revenue
                </Typography>
              },
              {
                selector:'.tactical',
                content: <Typography variant="subtitle1">
                  The tactical information tab will tell you more about the "where", "how" and "what" questions.
                </Typography>
              },
              {
                action: () => history.push({pathname: '/treemap',state: [true]})
                
              },
              {
                selector:'.treemapbuttons',
                content: <Typography variant="subtitle1">
                  The "where" section allows you to study the sales development on market, country and vendor level
                </Typography>
              },
              {
                content: <div>
                <Box fontWeight="fontWeightBold" align="center">Be aware!</Box> 
                <br></br>
                <Typography variant="subtitle1">
                  The presented sales are an estimation based on the reviews on the marketplace. Since these differ in 
                  quality and precision per marketplace, it is adviced to read the information section, which can be 
                  opened by clicking a similar icon to the one below. These can be found throughout the dashboard and
                  provide you with extra information.
                </Typography>
                <InfoOutlinedIcon align="center" style={{color:'#1092dd', fontSize:30}} />
                </div>
              },
              {
                action: () => history.push({pathname: '/mo',state: [true]})
                
              },
              {
                content: <Typography variant="subtitle1">
                  The "how" section provides you with information related to the business plan of vendors. 
                </Typography>
              },
              {
                selector:'.mobuttons',
                content: <Typography variant="subtitle1">
                  By clicking on a tab, a specific part of the business plan of vendors gets highlighted. 
                  Comparisons between countries and marketplaces can be made.
                </Typography>
              },
              {
                action: () => history.push({pathname: '/product',state: [true]})
                
              },
              {
                content: <Typography variant="subtitle1">
                  The "what" page allows you to study the types of products that are shipped from specific countries
                  and marketplaces. By clicking on the drug categories in the table below you can see what drugs
                  belong to a certain category.
                </Typography>
              },
              {
                content: <Typography variant="subtitle1">
                 Lastly, the dashboard also provides you with intelligence. By combining various information sources,
                 intelligence can enhance decision-making capabilities. This process often involves effort from you,
                  the analysts. To aid you with this process, this dashboard allows you to store your relevant
                 insights and share these with others, learning from each other. 
                </Typography>
              },
              {
                selector:'.commentButton',
                content: <Typography variant="subtitle1">
                  When clicking on this icon, a comment section appears. Once you have logged in, you can comment, reply
                  and like other comments. Together we know more!
                </Typography>
              },
              {
                selector:'.mindmap',
                content: <Typography variant="subtitle1">
                 Additionally, clicking over here allows you to create a mindmap that only you can see, keeping track of
                 the insights you have obtained.
                </Typography>
              },
              {
                selector:'.mindmap',
                content: <Typography variant="subtitle1">
                 That was the tour! You will now be redirected to the overview page, giving you an initial impression
                 of what you can expect.
                </Typography>
              },
              {
                action: () => history.push({pathname: '/overview'})
                
              },
          
          ];
  
  
    // Define column names. 'field' should be equal to the naming within the loaded data
    const columns = [
      {title: 'Timestamp', field:'timestamp'},
      {title:"Market", field:"market"},
      {title: 'Drug name', field:'name'},
      {title: "Vendor name", field:'vendor'},
      {title:"Ships from", field:"ships_from"},
      {title: 'Ships to', field:'ships_to'},
      {title: 'Category', field:'category'},
      {title:"Price in €", field:"price"}
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
        runIt()
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
          
       <MaterialTable className="producttable" title="Product table"
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
      onRowClick={(event, rowData, togglePanel) => {setProductInfo(rowData['name']); handleClickOpen()}}
         
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
            
            <DialogContent>
              <DialogContentText id="alert-dialog-slide-description">
              <Typography variant="body2">
              {productInfo}
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
      <Tour
                    steps={steps}
                    isOpen={isTourOpen}
                    onRequestClose={() => setIsTourOpen(false)}
                    startAt={5}
                    rounded={10}
                     />
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

export default ProductTable;


