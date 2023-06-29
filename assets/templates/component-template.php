<?php

namespace Block;

use App\Classes\Block;

class %blockname% extends Block
{

  public function __construct()
  {
    $this->name = '%name%';
    $this->title = '%title%';
    $this->description = '%description%';
    $this->view = 'components.%view%.%name%';
    $this->rootDir = '%rootDir%';
  }

  public static function registerFields(): array
  {
    return [

    ];
  }

}
