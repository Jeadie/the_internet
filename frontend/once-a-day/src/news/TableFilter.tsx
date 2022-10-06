import React from 'react';
import './App.css';
import Select, { MultiValue, ActionMeta } from 'react-select';

interface TableFilterProps {
  sources: string[]
  onChange: (v: string[]) => void;
  isDisabled: boolean
}

interface TableFilterState {
  selectedSources: string[]
}

interface SelectSource {
  label: string
  value: string
}

export class TableFilter extends React.Component<TableFilterProps, TableFilterState> {
  constructor(props: TableFilterProps) {
    super(props)
    this.state = {
      selectedSources: []
    }
  }

  componentDidUpdate() {
    console.log(this.state)
  }

  render() {
    const options: SelectSource[] = this.props.sources.map((x) => {
      return {label: x as string, value: x}
    })

    return (
      <Select
        isMulti
        placeholder={<p>Select Newspaper</p>}
        onChange={(newValue: MultiValue<SelectSource>, actionMeta: ActionMeta<SelectSource>) => {
          const values = newValue.map((x) => x.label)
          this.setState({selectedSources: values})
          this.props.onChange(values)
        }}
        options={options}
        className="basic-multi-select md:w-auto w-screen"
        classNamePrefix="select"
        isDisabled={this.props.isDisabled}
    />
    )
  }
}