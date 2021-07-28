
import React, {useState, useContext} from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Anita3 from './anita3.png'
import { createMuiTheme,ThemeProvider } from "@material-ui/core/styles";
import {BrowserRouter as Router, Route, Link} from 'react-router-dom';
import Box from '@material-ui/core/Box';
import Particles from "react-particles-js"
import Button from '@material-ui/core/Button';
import ButtonGroup from '@material-ui/core/ButtonGroup';
import { useHistory } from "react-router-dom";
//import {IntelligenceContext} from './IntelligenceContext'
import Grid from '@material-ui/core/Grid';
import OndemandVideoIcon from '@material-ui/icons/OndemandVideo';
import VideoPlayer from 'react-video-js-player'
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import Tour from 'reactour'




// Make sure particles are everywhere on the page & things are alligned in the center
const useStyles = makeStyles({
    particlesCanvas : {
        position : "absolute"
    },
    textContainer: {
        textAlign: 'center',
    },

    
})


  


export default function Home() {

    const classes = useStyles();
    const history = useHistory();


    const [open, setOpen] = useState(false);
    const [isTourOpen, setIsTourOpen] = useState(false);

    const handleClickOpen = () => {
        setOpen(true);
      };
    
    const handleClose = (event) => {
        
        setOpen(false);
        
      };

    const doTheTour = () => {
        window.location.href='/treemap'
       
    } 
    const steps = [
         
        {
          content: 'This is my first Step',
          action: () => history.push({pathname: '/overview',state: [true]})
          
        },
        {
          content: 'Welcome to the Anita dashboard! This tour will tell you all you need to know to get going.',
        },
      
      ];
      
    

  return (
    <div className='gek'>
        {/* RESPONSIBLE FOR RENDERING THE PARTICLES */}
    <Particles canvasClassName={classes.particlesCanvas}
    params={{
    particles:{
        number: {
            value: 45,
            density: {
                enable:true,
                value_area: 900
            }
        },
        shape: {
            type: 'circle',
            strole: {
                width: 1,
                color:'tomato'
            }
        },
        size: {
            value: 8,
            random: true,
            anim: {
                enable: true,
                speed: 10,
                size_min: 0.1,
                sync:true
            } 
        }
    }}}></Particles>
    <Grid container direction="column" justify="center" alignItems="center" spacing={5}>
      <Grid item xs={4} style={{ position: "relative", top: "200px"}}>
      <Box className={classes.imageContainer}>
        <img src={Anita3} style={{width: 300, height: 120}}></img>
    </Box>
      </Grid>
    
      <Grid item xs={4} style={{ position: "relative", top: "200px"}}>
          <Box class="center-frontpage">
          <div style={{color:"white"}}><font size="4"> 
          This dashboard provides you with information regarding drug trafficking on the dark web. 
          It is organised by means of the <b>5 W's of investigation</b>:</font></div>
            <br></br>
              <div style={{color:"white"}}><font size="5"> <b>W</b> </font><font size="4">ho - are the most interesting vendors? </font></div>
              <div style={{color:"white"}}><font size="5"> <b>W</b> </font><font size="4">here - are vendor hotspots? </font></div>
              <div style={{color:"white"}}><font size="5"> <b>W</b> </font><font size="4">hen - do changes occur in time? </font></div>
              <div style={{color:"white"}}><font size="5"> <b>W</b> </font><font size="4">hat - are the most sold drugs? </font></div>
              <div style={{color:"white"}}><font size="4"> Ho </font><font size="5"> <b>w</b> </font><font size="4">- do vendors do business? </font></div>
              
              
    
          </Box>
      </Grid>
      <Grid item xs={4} style={{ position: "relative", top: "200px"}}>
      <Grid container
          direction="row"
          justify="space-between"
          alignItems="center" spacing={2}>
      
      <Grid container direction="column" spacing={2}>
      <Grid align="center">
      <Button variant="contained" size="large" style={{color:'#1092dd'}}  onClick={() => {setIsTourOpen(true)}}>Start tour</Button>
                    <Tour
                    steps={steps}
                    isOpen={isTourOpen}
                    onRequestClose={() => setIsTourOpen(false)}
                    rounded={10}
                     /></Grid>
                     <br></br>
      <Grid align="center">
          <Button variant="contained" style={{color:'#1092dd'}} onClick={event =>  {window.location.href='/overview'}}>Dashboard</Button>
      </Grid>
      </Grid>
      </Grid>
       
    </Grid>

    </Grid>
    
    
    </div>


    
  );
}

