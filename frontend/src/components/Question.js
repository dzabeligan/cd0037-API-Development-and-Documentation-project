import React, { Component } from 'react';
import '../stylesheets/Question.css';

class Question extends Component {
  constructor() {
    super();
    this.state = {
      visibleAnswer: false,
    };
  }

  flipVisibility() {
    this.setState({ visibleAnswer: !this.state.visibleAnswer });
  }

  render() {
    const DEFAULT_IMAGE = 'art'
    const { question, answer, category, difficulty } = this.props;
    return (
      <div className='Question-holder'>
        <div className='Question'>{question}</div>
        <div className='Question-status'>
          <img
            className='category'
            alt={`${category ? category.toLowerCase() : DEFAULT_IMAGE}`}
            src={`${category ? category.toLowerCase() : DEFAULT_IMAGE}.svg`}
          />
          <div className='difficulty'>Difficulty: {difficulty}</div>
          <img
            src='delete.png'
            alt='delete'
            className='delete'
            onClick={() => this.props.questionAction('DELETE')}
          />
        </div>
        <div
          className='show-answer button'
          onClick={() => this.flipVisibility()}
        >
          {this.state.visibleAnswer ? 'Hide' : 'Show'} Answer
        </div>
        <div className='answer-holder'>
          <span
            style={{
              visibility: this.state.visibleAnswer ? 'visible' : 'hidden',
            }}
          >
            Answer: {answer}
          </span>
        </div>
      </div>
    );
  }
}

export default Question;
