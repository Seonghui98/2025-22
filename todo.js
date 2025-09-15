let todos = [];

function addTodo(task) {
  todos.push({ task: task, done: false });
}

function completeTodo(index) {
  if (todos[index]) todos[index].done = true;
}

addTodo("공부하기");
addTodo("산책하기");
completeTodo(0);

console.log(todos);
