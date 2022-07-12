import React, { Component } from 'react';
import $ from 'jquery';
import '../stylesheets/FormView.css';

class FormView extends Component {
  constructor(props) {
    super();
    this.state = {
      question: '',
      answer: '',
      difficulty: 1,
      category: 'none',
      categories: {},
      newCategory: ''
    };
  }

  componentDidMount() {
    $.ajax({
      url: `/categories`, //TODO: update request URL
      type: 'GET',
      success: (result) => {
        this.setState({ categories: result.categories });
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again');
        return;
      },
    });
  }

  submitQuestion = (event) => {
    event.preventDefault();
    $.ajax({
      url: '/questions', //TODO: update request URL
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        question: this.state.question,
        answer: this.state.answer,
        difficulty: this.state.difficulty,
        category: this.state.category,
        newCategory: this.state.newCategory,
      }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById('add-question-form').reset();
        return;
      },
      error: (error) => {
        alert('Unable to add question. Please try your request again');
        return;
      },
    });
  };

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  render() {
    return (
      <div id='add-form'>
        <h2>Add a New Trivia Question</h2>
        <form
          className='form-view'
          id='add-question-form'
          onSubmit={this.submitQuestion}
        >
          <label>
            Question
            <input required type='text' name='question' onChange={this.handleChange} />
          </label>
          <label>
            Answer
            <input required type='text' name='answer' onChange={this.handleChange} />
          </label>
          <label>
            Difficulty
            <select required name='difficulty' onChange={this.handleChange}>
              <option value='1'>1</option>
              <option value='2'>2</option>
              <option value='3'>3</option>
              <option value='4'>4</option>
              <option value='5'>5</option>
            </select>
          </label>
          <label>
            Category
            <select required name='category' onChange={this.handleChange}>
              <option value='none' selected disabled hidden>Select a category</option>
              {Object.keys(this.state.categories).map((id) => {
                return (
                  <option key={id} value={id}>
                    {this.state.categories[id]}
                  </option>
                );
              })}
              <option value='other'>Other</option>
            </select>
          </label>
          <label
            style={{
              visibility:
                this.state.category === 'other' ? 'visible' : 'hidden',
            }}
          >
            New Category
            <input
              type='text'
              name='newCategory'
              onChange={this.handleChange}
              required={this.state.category === 'other'}
            />
          </label>
          <input disabled={this.state.category === 'none'} type='submit' className='button' value='Submit' />
        </form>
      </div>
    );
  }
}

export default FormView;
