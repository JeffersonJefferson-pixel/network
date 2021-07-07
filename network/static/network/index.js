var active_username = '';
var visiting_username = '';


document.addEventListener('DOMContentLoaded', function() {
  active_username = document.querySelector('#active_username').innerText;
  document.querySelector('#all_post').addEventListener('click', load_index);
  document.querySelector('#active_username').addEventListener('click', load_profile);
  document.querySelector('#following').addEventListener('click', load_following);

  //default
  load_index();
})

function load_following() {

  //
  document.querySelector('#profile_view').style.display = 'none';
  document.querySelector('#post_view').style.display = 'block';
  document.querySelector('#create_post_view').style.display = 'none'

  get_post('following')
}

function load_profile(e) {
  
  //toggle views
  document.querySelector('#profile_view').style.display = 'block';
  document.querySelector('#post_view').style.display = 'block';
  document.querySelector('#create_post_view').style.display = 'none';

  visiting_username = e.target.innerText.toLowerCase();
  get_user(visiting_username)
  get_post(visiting_username)
}

function load_index() {

  //toggle views
  document.querySelector('#create_post_view').style.display = 'block';
  document.querySelector('#post_view').style.display = 'block';
  document.querySelector('#profile_view').style.display = 'none';

  document.querySelector('#create_post_form').onsubmit = create_post;
  get_post('all');

}

function get_user(username) {
  fetch(`/users/${username}`)
  .then(response => response.json())
  .then(result => {
    console.log(result);

    document.querySelector('#profile_username').innerHTML = result[0].username;
    document.querySelector('#num_follower').innerHTML = result[0].num_follower;
    document.querySelector('#num_following').innerHTML = result[0].num_following;

    document.querySelector('#profile_username').addEventListener('click', load_profile)

    if(active_username !== username & !result[1].is_following) {
      document.querySelector('#follow_button').style.display = 'block';
      document.querySelector('#follow_button').addEventListener('click', follow);
    }else{
      document.querySelector('#follow_button').style.display = 'none';
    }
  }) 
}

function get_post(username) {
  fetch(`/posts/${username}`)
  .then(response => response.json())
  .then(posts => {
    console.log(posts);

    document.querySelector('#post_view');
    post_view.innerHTML = '';

    posts.forEach(function(post) {
      const post_container = document.createElement('div');
      post_container.className = "post_container";
      post_container.setAttribute('id', post.id);
      
      const poster = document.createElement('div');
      const edit = document.createElement('div');
      const content = document.createElement('div');
      const timestamp = document.createElement('div');
      const like_div = document.createElement('div');
      const like_btn = document.createElement('i');
      const like_num = document.createElement('div');
      const comment = document.createElement('div');

      poster.className = "username";
      edit.className = "edit";
      timestamp.className = "timestamp";
      like_div.className = "like_div"

      if(post.liked) {
        like_btn.className = "fa fa-heart unlike"
        like_btn.onclick = unlike;
      }else {
        like_btn.className = "fa fa-heart like"
        like_btn.onclick = like;
      }
      
      like_num.className = "like_num";
      comment.className = "comment";

      poster.innerHTML = post.poster;
      edit.innerHTML = 'Edit';
      content.innerHTML = post.content;
      timestamp.innerHTML =post.timestamp;
      like_num.innerHTML = `${post.like}`;
      comment.innerHTML =  'Comment';

      poster.addEventListener('click', load_profile);
      

      like_div.appendChild(like_btn);
      like_div.appendChild(like_num);

      post_container.appendChild(poster);
      post_container.appendChild(edit);
      post_container.appendChild(content);
      post_container.appendChild(timestamp);
      post_container.appendChild(like_div);
      post_container.appendChild(comment);

      post_view.append(post_container);
    })
  })
}

function create_post() {
    
    const content = document.querySelector('#new_post_content')
    //request post
    fetch('/posts', {
        method: 'POST',
        body: JSON.stringify({
            content: content.value
        })
    })
    .then(response => response.json())
    .then(result => {
      //print result
      console.log(result);
    })
    .catch(error => {
      console.log('Error:', error);
    });

    return false
}

function follow() {
  //Post follow request
  fetch('/users/follow', {
    method: 'POST',
    body: JSON.stringify({
      following: visiting_username
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result)
  })
  .catch(error => {
    console.log('Error:', error);
  });

  return false;
}

function like(e) {

  let post_id = e.target.parentNode.parentNode.id;
  const like_num = document.getElementById(post_id).getElementsByClassName('like_num')[0];
  
  fetch(`/posts/like/${post_id}`, {
    method: 'POST',
    body: JSON.stringify({}) 
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
    e.target.className = "fa fa-heart unlike";
    like_num.innerHTML = parseInt(like_num.innerHTML) + 1;
    e.target.onclick = unlike;
  })
  .catch(error => {
    console.log("Error:", error);
  });

  return false;
}

function unlike(e) {
  
  let post_id = e.target.parentNode.parentNode.id;
  const like_num = document.getElementById(post_id).getElementsByClassName('like_num')[0];  
  
  fetch(`/posts/unlike/${post_id}`, {
    method: 'POST',
    body: JSON.stringify({}) 
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
    e.target.className = "fa fa-heart like";
    like_num.innerHTML = parseInt(like_num.innerHTML) - 1;
    e.target.onclick = like;
  })
  .catch(error => {
    console.log("Error:", error);
  });

  return false;

}