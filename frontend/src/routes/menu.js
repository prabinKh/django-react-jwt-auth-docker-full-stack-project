import { VStack, Text, Button } from "@chakra-ui/react"

import { useEffect, useState } from "react"

import { get_notes } from "../api/endpoints"

import { useAuth } from "../context/useAuth";

const Menu = () => {

    const [notes, setNotes] = useState([])
    const { user, logoutUser } = useAuth();

    useEffect(() => {
        const fetchNotes = async () => {
            const notes = await get_notes();
            setNotes(notes)
        }
        fetchNotes();
    }, [])

    const handleLogout = async () => {
        await logoutUser()
    };

    return (
        <VStack alignItems='start'>
            <Text fontSize='42px' pb='30px'>Welcome {user ? user.username : 'Guest'} 👋</Text>
            <VStack alignItems='start' pb='50px'>
                {notes.map((note) => {
                    return (
                        <VStack key={note.id} alignItems='start' spacing={1}>
                            <Text fontSize='22px' fontWeight='bold'>{note.name}</Text>
                            <Text fontSize='16px'>{note.description}</Text>
                        </VStack>
                    );
                })}
            </VStack>
            <Button onClick={handleLogout} colorScheme='red'>Logout</Button>
        </VStack>
    )
}

export default Menu;