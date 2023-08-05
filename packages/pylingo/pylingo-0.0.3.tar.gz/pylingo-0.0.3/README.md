# pylingo

General purpose extensible configuration language.

```bash

config {
  {key} = { object | array | scalar }
}

import "{name}" {
  version = "~> 1.16"
  module  = "{scalar}"
}

variable "{name}" {
	{key} = { object | array | scalar }
}

data "{source}" "{name}" {
    {key} = { object | array | scalar }
}


#create event log group
generator "{type}" "{name}" {
  {key} = { object | array | scalar }
}



```