import React, { Component,useEffect, useState,useContext } from 'react';
import {BrowserRouter as Router, Route, Link} from 'react-router-dom';
import Home from './Home';
import Knowledge from './components/Knowledge';
import HOW from './components/HOW';
import Comments from './components/Comments'
import WHERE from './components/WHERE';
import Overview from './components/Overview'
import './App.css'
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import Appbar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Box from '@material-ui/core/Box';
import anita_logo from './anita_logo.png';
import VendorTable from "./components/VendorTable";
import ProductTable from "./components/ProductTable";
import ReviewTable from "./components/ReviewTable";
import TextAnalysisTable from "./components/TextAnalysisTable";
import WHO from "./components/WHO";
import PersonIcon from '@material-ui/icons/Person';
import { makeStyles } from "@material-ui/core/styles";
import { GiMedicines } from "react-icons/gi";
import { IoLocationSharp } from "react-icons/io5";
import { MdBusinessCenter } from "react-icons/md"
import { MdRateReview } from "react-icons/md"
import { BsFileText } from "react-icons/bs";
import { CgNotes } from "react-icons/cg";
import Dialog from '@material-ui/core/Dialog';
import Button from '@material-ui/core/Button';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import Draggable from 'react-draggable';
import Paper from '@material-ui/core/Paper';
import WHAT from './components/WHAT'


const useStyles = makeStyles(theme => ({
  rightAlign: {
    marginLeft: 'auto',
    
  }
}));




function App() {

  console.log('APP')
  console.log("http://" + process.env.REACT_APP_BACKEND_HOST + ":" + process.env.REACT_APP_BACKEND_PORT + "/product")
  console.log(process.env.REACT_APP_BACKEND_HOST + ":" + process.env.REACT_APP_BACKEND_PORT);

  const classes = useStyles()
  // These are the routes to the various functionalities
  const routesFirstTab = ['Tactical', 'Data','Overview']
  const routes = ['/sales','/network','/map','/knowledge', '/MO', '/treemap', '/bestMO', '/product', '/operational', '/vendortable', '/producttable', '/reviewtable', '/textanalysistable', '/overview']

  const [value, setValue] = React.useState(0);
  const [valueFirstTab, setValueFirstTab] = React.useState('Overview');
  const [selectedVendor, setSelectedVendor] = useState('kaasjes');
  const [openMindmap, setOpenMindmap] = useState(false);

  // This useEffect is declared to higlight the right button once a user clicks refresh
  useEffect(() => {
    let path = window.location.pathname;
    if (path === '/product'){
      setValueFirstTab('Tactical')
      setValue('/product')
    }
    if (path === '/treemap'){
      setValueFirstTab('Tactical')
      setValue('/treemap')
    }
    if (path === '/operational'){
      setValueFirstTab('Tactical')
      setValue('/operational')
    }
    if (path === '/MO'){
      setValueFirstTab('Tactical')
      setValue('/MO')
    }
    if (path === '/vendortable'){
      setValueFirstTab('Data')
      setValue('/vendortable')
    }
    if (path === '/producttable'){
      setValueFirstTab('Data')
      setValue('/producttable')
    }
    if (path === '/reviewtable'){
      setValueFirstTab('Data')
      setValue('/reviewtable')
    }
    if (path === '/textanalysistable'){
      setValueFirstTab('Data')
      setValue('/textanalysistable')
    }
    if (path === '/overview'){
      setValue('/overview')
    }

  }, []);


    // Set design configurations
    const theme = createMuiTheme({
        palette: {
          primary: {
            main: '#1092dd',
          },
          secondary: {
            main: '#FFFFF',
          }
        },
        notActiveTab:{
          fontSize:'13px',
          color:'white'
        },
        activeTab:{
          fontSize:'16px',
          fontStyle: 'italic',
          fontWeight:'bold',
          color:'white'
        }
      });

      const theme2 = createMuiTheme({
        palette: {
          primary: {
            main: '#FFFFF',
          },
          secondary: {
            main: '#1092dd',
          }
        },
      });

    // Handles the change of the top bar
    const handleChangeFirst = (event, newValue) => {
      console.log(newValue)
      setValueFirstTab(newValue);
      if (newValue === "Overview"){
        setValue('/overview')
      }
      if (newValue === "Tactical"){
        setValue('/treemap')
      }
      // if (newValue === "Operational"){
      //   setValue('/operational')
      // }
      if (newValue === "Data"){
        setValue('/vendortable')
      }

    };

    const handleChangeSecond = (event, newValue) => {
      setValue(newValue);
      };
  
      const handleClickOpenMindmap = () => {
        setOpenMindmap(true);
      };
    
    const handleCloseMindmap = (event) => {
        
      setOpenMindmap(false);
        
      };

     

      function PaperComponent(props) {
        return (
          <Draggable handle="#draggable-dialog-title" cancel={'[class*="MuiDialogContent-root"]'}>
            <Paper {...props} />
          </Draggable>
        );
      }
      

    return (
      <div className="ok">
        <MuiThemeProvider theme={theme}>
   
      

      <Appbar position="static">          
      <Tabs value={value} onChange={handleChangeFirst} aria-label="simple tabs example">
                  <Box >
                      <img src={anita_logo} style={{width: 100, height: 40}} onClick={event =>  window.location.href='/'}></img>
                  </Box>
                  <Tab style={valueFirstTab === "Overview" ? theme.activeTab : theme.notActiveTab} label="Overview"  value={routesFirstTab[2]} component={Link} to={routes[13]}></Tab>
                  <Tab className="tactical" style={valueFirstTab === "Tactical" ? theme.activeTab : theme.notActiveTab} label="Information"  value={routesFirstTab[0]} component={Link} to={routes[5]}></Tab>
                  <Tab className="data" style={valueFirstTab === "Data" ? theme.activeTab : theme.notActiveTab} label="Raw data" value={routesFirstTab[1]} component={Link} to={routes[9]}/>
                 <Tab icon={< CgNotes size={30}/>} style={{color:'white'}} onClick={handleClickOpenMindmap}  value={valueFirstTab} className = {classes.rightAlign}></Tab>
                 
                      <Dialog
                            open={openMindmap}
                            onClose={handleCloseMindmap}
                            aria-labelledby="draggable-dialog-title"
                            aria-describedby="alert-dialog-description"  maxWidth={"xl"}
                            PaperComponent={PaperComponent}
                            fullWidth = {true}
                        >
                                         
                  <DialogTitle id="draggable-dialog-title">{"Create your mindmap - this screen is draggable"} 
                  </DialogTitle>
                  
                    <DialogContent>
                      <Knowledge/>
                    </DialogContent>
                    <DialogActions>
                      <Button onClick={handleCloseMindmap} color="primary">
                        Close
                      </Button>
                      
                    </DialogActions>
                            
                        </Dialog>
                  
                 </Tabs>
                 </Appbar>
                 
                 
      {/* DETERMINES WHAT SECOND BAR SHOULD BE SHOWN IF INFORMATION IS CLICKED */}
        {valueFirstTab === 'Tactical'? 
        <MuiThemeProvider theme={theme2}>
        <Appbar position="static">          
        <Tabs value={value} onChange={handleChangeSecond} aria-label="example">
       
                  <Tab  icon={< IoLocationSharp size={20} />}label="Where?"   value={routes[5]} component={Link} to={routes[5]}/>
                    <Tab icon={< MdBusinessCenter size={20} />} label="How?"  value={routes[4]} component={Link} to={routes[4]}/>
                    <Tab icon={<GiMedicines size={20} />} label="What?"   value={routes[7]} component={Link} to={routes[7]}/>
                    <Tab icon={<PersonIcon />} label="Who?" value={routes[8]} component={Link} to={routes[8]}/>
                 </Tabs>

        
                 </Appbar>
                 </MuiThemeProvider>
        
        :
        <div></div>}

    {/* DEFINES WHAT SECOND BAR SHOULD BE SHOW IF DATA IS CLICKED */}
    {valueFirstTab === 'Data'? 
        <MuiThemeProvider theme={theme2}>
        <Appbar position="static">          
        <Tabs value={value} onChange={handleChangeSecond} aria-label="example">
       
                  <Tab  icon={<PersonIcon />} label="Vendors"   value={routes[9]} component={Link} to={routes[9]}/>
                    <Tab icon={<GiMedicines size={20} />} label="Products"  value={routes[10]} component={Link} to={routes[10]}/>
                    <Tab icon={<MdRateReview size={20} />} label="Reviews"   value={routes[11]} component={Link} to={routes[11]}/>
                    <Tab icon={<BsFileText size={20} />} label="Text analysis"   value={routes[12]} component={Link} to={routes[12]}/>
                 </Tabs>

        
                 </Appbar>
                 </MuiThemeProvider>
        
        :
        <div></div>}
      
                  
                
                 <Route exact path="/" component={Home} />
                 <Route exact path="/MO" component={HOW} />
                 <Route exact path="/treemap" component={WHERE} />
                 <Route exact path="/Product" component={WHAT}/>
                 <Route path="/operational" component={WHO}/>
                 <Route exact path='/knowledge' component ={Knowledge}/>
                 <Route exact path='/comments' component ={Comments}/>
                 <Route exact path='/vendortable' component ={VendorTable}/>
                 <Route exact path='/producttable' component ={ProductTable}/>
                 <Route exact path='/reviewtable' component ={ReviewTable}/>
                 <Route exact path='/textanalysistable' component ={TextAnalysisTable}/>
                 <Route exact path='/overview' component ={Overview}/>
                 </MuiThemeProvider> 
                
               </div>
    )
  
}

export default App;
