import { useState, useEffect } from "react";
import {
  Modal,
  Row,
  TextInput,
  Column,
  DatePicker,
  DatePickerInput,
  TextArea,
} from "@carbon/react";

interface Props {
  open: boolean;
  modalHeading: string;
  setOpen: Function;
  modalLabel: string;
  action: string;
  addEvent: Function;
  selectedEventForModal: any;
  isEdit: Boolean;
  userDetails: Object;
  setUserDetails?: Function;
}

const ModalAddEdit: React.FunctionComponent<Props> = (props) => {
  console.log('userDetails props', props.userDetails)
  // Convert date for display in DatePicker format (mm/dd/yyyy)
  const formatDateToPicker = (date: string) => {
    const cleanDate = date.replace(/\d+(st|nd|rd|th)/, (match) => match.slice(0, -2));
    const d = new Date(cleanDate);

    if (isNaN(d.getTime())) {
      console.log("Invalid date:", date);
      return "";
    }

    const month = (d.getMonth() + 1).toString().padStart(2, "0");
    const day = d.getDate().toString().padStart(2, "0");
    const year = d.getFullYear();
    return `${month}/${day}/${year}`; // MM/DD/YYYY format
  };

  // Helper function to format date back to "3rd March 2025"
  const formatDate = (date: string) => {
    const d = new Date(date);
    const day = d.getDate();
    const month = d.toLocaleString("default", { month: "long" });
    const year = d.getFullYear();

    // Function to add ordinal suffix (st, nd, rd, th)
    const getOrdinalSuffix = (day: number) => {
      if (day > 3 && day < 21) return "th";
      switch (day % 10) {
        case 1:
          return "st";
        case 2:
          return "nd";
        case 3:
          return "rd";
        default:
          return "th";
      }
    };
    return `${day}${getOrdinalSuffix(day)} ${month} ${year}`;
  };

  const { selectedEventForModal, isEdit } = props;
  console.log('selectedEventForModal', selectedEventForModal);
  const [name, setName] = useState(isEdit ? selectedEventForModal.event_name : "");
  const [location, setLocation] = useState(isEdit ? selectedEventForModal.event_location : "");
  const [date, setDate] = useState(isEdit ? formatDateToPicker(selectedEventForModal.event_date) : "");
  const [description, setDescription] = useState(isEdit ? selectedEventForModal.event_description : "");

  useEffect(() => {
    if (isEdit && selectedEventForModal) {
      setName(selectedEventForModal.event_name);
      setLocation(selectedEventForModal.event_location);
      setDate(formatDateToPicker(selectedEventForModal.event_date)); // Convert date back
      setDescription(selectedEventForModal.event_description);
    }
  }, [isEdit, selectedEventForModal]);

  const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => setName(e.target.value);
  const handleLocationChange = (e: React.ChangeEvent<HTMLInputElement>) => setLocation(e.target.value);
  const handleDateChange = (date: any) => setDate(date); // DatePicker gives date in specific format
  const handleDescriptionChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => setDescription(e.target.value);

  // Handle save button click
  const handleSave = async () => {
    const formattedDate = formatDate(date); // Format the date before saving
    const eventData = {
      event_id: isEdit ? selectedEventForModal.event_id : Math.floor(Math.random() * 900) + 101,
      event_name: name,
      event_description: description,
      event_location: location,
      event_date: formattedDate, // Save formatted date back
    };

    console.log("on save event", eventData);

    if (isEdit) {
      // If editing, update the existing event in the parent state
      props.addEvent(eventData); // Parent function should handle event update
    } else {
      // If adding a new event
      props.addEvent(eventData);
    }
 

    props.setOpen(false); // Close the modal
  };

  return (
    <Modal
      open={props.open}
      onRequestClose={() => props.setOpen(false)}
      hasScrollingContent
      modalHeading={props.modalHeading}
      modalLabel={props.modalLabel}
      primaryButtonText={props.action}
      secondaryButtonText="Cancel"
      onRequestSubmit={handleSave} // Trigger save on submit
    >
      <Row>
        <Column>
          <TextInput
            data-modal-primary-focus
            id="text-input-1"
            labelText="Name"
            placeholder="Enter Name"
            value={name}
            onChange={handleNameChange}
            style={{ marginBottom: "1rem" }}
          />
        </Column>
      </Row>

      <Row style={{ marginTop: "2rem" }}>
        <Column>
          <DatePicker
            datePickerType="single"
            onChange={handleDateChange}
            dateFormat="m/d/Y"
          >
            <DatePickerInput
              placeholder="mm/dd/yyyy"
              labelText="Date of event"
              id="date-picker-single"
              size="md"
              defaultValue={date} // Pass date state to the input field
            />
          </DatePicker>
        </Column>
        <Column>
          <TextInput
            id="text-input-2"
            labelText="Location"
            placeholder="Enter Location"
            value={location}
            onChange={handleLocationChange}
            style={{ marginBottom: "1rem" }}
          />
        </Column>
      </Row>

      <Row style={{ marginTop: "2rem" }}>
        <Column>
          <TextArea
            labelText="Description of the event"
            placeholder="Enter description here"
            rows={2}
            value={description}
            onChange={handleDescriptionChange}
          />
        </Column>
      </Row>
    </Modal>
  );
};

export default ModalAddEdit;
