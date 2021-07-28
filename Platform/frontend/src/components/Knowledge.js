// All import statements
import React, { useState, useRef, useEffect, useCallback } from 'react';
import ReactFlow, {
  ReactFlowProvider,
  addEdge,
  removeElements,
  Controls,
  Background,
  useStoreState 
} from 'react-flow-renderer';

import Button from '@material-ui/core/Button';
import localforage from 'localforage';
import Typography from '@material-ui/core/Typography';
import ButtonGroup from '@material-ui/core/ButtonGroup';
import { makeStyles,createMuiTheme,ThemeProvider } from '@material-ui/core/styles';
import Popoverside from '../atoms/Popoverside';
import SaveIcon from '@material-ui/icons/Save';
import { IconButton } from '@material-ui/core';
import OndemandVideoIcon from '@material-ui/icons/OndemandVideo';

import Video from '../mindmap.mp4'
import VideoPlayer from 'react-video-js-player'
import Dialog from '@material-ui/core/Dialog';



const flowKey = 'example-flow';
let id = 0;
const getId = () => `${id++}`;


// Set colours
const DnDFlow = () => {

  const theme = createMuiTheme({
    palette: {
      primary: {
        main: '#1092dd',
      },
      secondary: {
        main: '#ff0072',
      }
    },
  });

  // Set useStates to allow the user to create elements
  const [open, setOpen] = useState(false);
  const reactFlowWrapper = useRef(null);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);
  const [elements, setElements] = useState([]);
  const [nodeName, setNodeName] = useState([]);
  const [nodeBg, setNodeBg] = useState([]);
  const [selectedId, setSelectedId] = useState([]);
  const [rfInstance, setRfInstance] = useState(null);

  const onSave = useCallback(() => {
    if (rfInstance) {
      const flow = rfInstance.toObject();
      localforage.setItem(flowKey, flow);
    }
  }, [rfInstance]);

  const handleClickOpen = () => {
    setOpen(true);
  };
const handleClose = (event) => {
    
    setOpen(false);
    
  };
 
  useEffect(() => {
    const data = window.localStorage.getItem('knowledge_field')
    const id_value = window.localStorage.getItem('knowledge_id')
    const nodeName = window.localStorage.getItem('nodename')
    const nodeColour = window.localStorage.getItem('nodecolour')
    setElements(JSON.parse(data))
    setNodeName(JSON.parse(nodeName))
    setNodeBg(JSON.parse(nodeColour))
    id = JSON.parse(id_value)
  },[])
  
  useEffect(() => {
    window.localStorage.setItem('knowledge_field', JSON.stringify(elements))
    window.localStorage.setItem('knowledge_id', JSON.stringify(id))
    window.localStorage.setItem('nodename', JSON.stringify(nodeName))
    window.localStorage.setItem('nodecolour', JSON.stringify(nodeBg))
    console.log(elements)
    // console.log(id)
    
  })

  
  //THE NAME EDIT PART!
  useEffect(() => {
    setElements((els) =>
        els.map((el) => {
          if (el.id === selectedId) {
            // it's important that you create a new object here
            // in order to notify react flow about the change
            el.data = {
              ...el.data,
              label: nodeName,
            };
          }
          return el;
        })
      );
  }, [nodeName, setElements]);



  useEffect(() => {
    setElements((els) =>
      els.map((el) => {
        if (el.id === selectedId) {
          // it's important that you create a new object here
          // in order to notify react flow about the change
          el.style = { ...el.style, backgroundColor: nodeBg };
        }
        return el;
      })
    );
  }, [nodeBg, setElements]);



  const NodesDebugger = () => {
    const selectedNode = useStoreState((state) => state.selectedElements)
    if (selectedNode !== null){
      setSelectedId(selectedNode[0].id)}
      if (selectedNode !== null){
        console.log(selectedNode[0].data.label)}
        
    return null;
  };





  const onConnect = (params) => setElements((els) => addEdge(params, els));
  const onElementsRemove = (elementsToRemove) =>
    setElements((els) => removeElements(elementsToRemove, els));
  const onLoad = (_reactFlowInstance) =>
    setReactFlowInstance(_reactFlowInstance);
  const onDragOver = (event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  };
  const onDrop = (event) => {
    event.preventDefault();
    const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();
    const type = event.dataTransfer.getData('application/reactflow');
    const position = reactFlowInstance.project({
      x: event.clientX - reactFlowBounds.left,
      y: event.clientY - reactFlowBounds.top,
    });
    const newNode = {
      id: getId(),
      type,
      position,
      data: { label: `${type} node` },
    };
    setElements((es) => es.concat(newNode));
  };

  //Handles draging nodes 
  const onDragStart = (event, nodeType) => {
    event.dataTransfer.setData('application/reactflow', nodeType);
    event.dataTransfer.effectAllowed = 'move';
  };
   


  function printContent(el) {
    var restorepage = document.body.innerHTML;
    console.log(restorepage)
    var printcontent = document.getElementsByClassName(el)[0].innerHTML;
    console.log(printcontent)
    document.body.innerHTML = printcontent;
    window.print();
    document.body.innerHTML= restorepage;
  }

  return (
    <div className="dndflow">
      <ThemeProvider theme={theme}>
      <br></br>
      <div className="knowledgepage" style={{width:1000}}>
      <ReactFlowProvider>
        <div className="reactflow-wrapper" ref={reactFlowWrapper} style={{height:600, width:800}} >
          <ReactFlow
            elements={elements}
            onConnect={onConnect}
            onElementsRemove={onElementsRemove}
            onLoad={onLoad}
            onDrop={onDrop}
            onDragOver={onDragOver}
            
          >
            <Background
              variant="dots"
              gap={15}
              size={1}
            />
            
            <NodesDebugger />
            <Controls />
          </ReactFlow>
          
        
        </div>
        <div className="chill" style={{width:160}}>
          
          <br></br>
          <div className="add_text">
          <Typography variant="h6" gutterBottom>
          Add 
          </Typography></div>
          <Button>
              <OndemandVideoIcon style={{color:'#FF6700'}} onClick={handleClickOpen} ></OndemandVideoIcon>
        </Button>
        <Dialog
                        open={open}
                        onClose={handleClose}
                        aria-labelledby="alert-dialog-title"
                        aria-describedby="alert-dialog-description"  maxWidth={"md"}
                    >
                        <VideoPlayer src={Video} width="720" height="420"></VideoPlayer>
                        
                    </Dialog>
          <div className="popover_knowledge">
          <Popoverside /></div>
          <ButtonGroup orientation="vertical">
          
          <Button variant="outlined" size="small" color="primary" onDragStart={(event) => onDragStart(event, 'input')} draggable >Research question</Button>
          <Button variant="outlined" size="small" onDragStart={(event) => onDragStart(event, 'default')} draggable >Hypothesis</Button>
          <Button variant="outlined" size="small" color="secondary" onDragStart={(event) => onDragStart(event, 'output')} draggable >Arguments</Button>
          </ButtonGroup>
          <br></br>
          <br></br>
          <Typography variant="h6" gutterBottom>
            Edit
          </Typography>
          <div className="updatenode__controls" style={{width:90}}>
          <label>Text</label>
          
          <input style={{width:160}}
            value={nodeName}
            onChange={(evt) => setNodeName(evt.target.value)}
          />
          
          <label className="updatenode__bglabel">Colour</label>
          
          <input style={{width:160}} value={nodeBg} onChange={(evt) => setNodeBg(evt.target.value)} />
          
          </div>
          <br></br>
          
                
          
          <IconButton aria-describedby={id} variant="contained" color="primary" onClick={() => window.print()} >
              <SaveIcon />
              </IconButton>
          
        </div> 
      </ReactFlowProvider>
      
      
    
    </div>
    </ThemeProvider>
    </div>
    
  );
};
export default DnDFlow;

