import React from 'react';
import { Card, FormGroup, TextArea, Button, Classes } from '@blueprintjs/core';
import { IconNames } from '@blueprintjs/icons';
import ReactMarkdown from 'react-markdown';

const Item = ({
  item: {
    body,
    url,
    media: { post_image }
  }
}) => (
  <Card className="search_item">
    {post_image && (
      <p>
        <img alt="" src={post_image} />
      </p>
    )}
    {body && <ReactMarkdown source={body} />}
    {url && (
      <p>
        <a href={url} target="_blank" rel="noopener noreferrer">
          {url}
        </a>
      </p>
    )}
    <div className="search_comment">
      <FormGroup>
        <TextArea className={Classes.FILL} />
      </FormGroup>
      <Button text="Add comment" icon={IconNames.COMMENT} />
    </div>
  </Card>
);

export default Item;
