import React from 'react';
import ReactDOM from 'react-dom';

class ContentFeed extends React.Component {
    
    constructor(props) {
    super(props);

    this.state = {
      posts: []
        }
        this.getPosts = this.getPosts.bind(this);
    }
    componentDidMount() {
        this.getPosts();
    }
    getPosts() {
    fetch('http://127.0.0.1:8000/friends/post/3/')
        .then(results => results.json())
        .then(results => {
        console.log(results)
        this.setState({posts: results});
        }
        )
    }

    render() {
    
    let output = Object.keys(this.state.posts).map((item, index) => {
           return (
           <div key = {index}>
            <li><b>{item}</b> : <i>{this.state.posts[item]}</i> </li>
           </div>
           );
           })
           
        return (
   
         

           <ul>
           {output}
            </ul>
    );   
    }}


ReactDOM.render(

    <ContentFeed />,
    document.getElementById("root")
    
);

