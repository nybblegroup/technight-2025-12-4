import { Router, Request, Response } from 'express';
import prisma from '../database';

const router = Router();

/**
 * @swagger
 * components:
 *   schemas:
 *     Example:
 *       type: object
 *       properties:
 *         id:
 *           type: integer
 *           description: Unique identifier for the example
 *         name:
 *           type: string
 *           maxLength: 200
 *           description: Name of the example
 *         title:
 *           type: string
 *           maxLength: 200
 *           description: Title of the example
 *         entryDate:
 *           type: string
 *           format: date-time
 *           description: Date when the example was entered
 *         description:
 *           type: string
 *           maxLength: 1000
 *           description: Optional description field
 *           nullable: true
 *         isActive:
 *           type: boolean
 *           description: Indicates if the example is active
 *           default: true
 *     CreateExampleDto:
 *       type: object
 *       required:
 *         - name
 *         - title
 *       properties:
 *         name:
 *           type: string
 *           maxLength: 200
 *           description: Name of the example
 *         title:
 *           type: string
 *           maxLength: 200
 *           description: Title of the example
 *         description:
 *           type: string
 *           maxLength: 1000
 *           description: Optional description field
 *           nullable: true
 *         isActive:
 *           type: boolean
 *           description: Indicates if the example is active
 *           default: true
 *     UpdateExampleDto:
 *       type: object
 *       properties:
 *         name:
 *           type: string
 *           maxLength: 200
 *           description: Name of the example
 *         title:
 *           type: string
 *           maxLength: 200
 *           description: Title of the example
 *         description:
 *           type: string
 *           maxLength: 1000
 *           description: Optional description field
 *           nullable: true
 *         isActive:
 *           type: boolean
 *           description: Indicates if the example is active
 */

/**
 * @swagger
 * /api/examples:
 *   get:
 *     summary: Get all examples
 *     description: Retrieves all example records from the database
 *     tags:
 *       - Examples
 *     responses:
 *       200:
 *         description: List of all examples
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/Example'
 */
router.get('/', async (req: Request, res: Response) => {
  try {
    const examples = await prisma.example.findMany({
      orderBy: {
        entryDate: 'desc',
      },
    });
    res.json(examples);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching examples', error: String(error) });
  }
});

/**
 * @swagger
 * /api/examples/search:
 *   get:
 *     summary: Search examples
 *     description: Search examples by name (case-insensitive)
 *     tags:
 *       - Examples
 *     parameters:
 *       - in: query
 *         name: name
 *         schema:
 *           type: string
 *         description: Name to search for
 *     responses:
 *       200:
 *         description: Search results
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/Example'
 */
router.get('/search', async (req: Request, res: Response) => {
  try {
    const { name } = req.query;

    const examples = await prisma.example.findMany({
      where: name
        ? {
            name: {
              contains: String(name),
              mode: 'insensitive',
            },
          }
        : undefined,
      orderBy: {
        entryDate: 'desc',
      },
    });

    res.json(examples);
  } catch (error) {
    res.status(500).json({ message: 'Error searching examples', error: String(error) });
  }
});

/**
 * @swagger
 * /api/examples/{id}:
 *   get:
 *     summary: Get example by ID
 *     description: Retrieves a specific example by its ID
 *     tags:
 *       - Examples
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *         description: The example ID
 *     responses:
 *       200:
 *         description: Example found
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Example'
 *       404:
 *         description: Example not found
 */
router.get('/:id', async (req: Request, res: Response) => {
  try {
    const id = parseInt(req.params.id);
    const example = await prisma.example.findUnique({
      where: { id },
    });

    if (!example) {
      return res.status(404).json({ message: `Example with ID ${id} not found` });
    }

    res.json(example);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching example', error: String(error) });
  }
});

/**
 * @swagger
 * /api/examples:
 *   post:
 *     summary: Create a new example
 *     description: Creates a new example record
 *     tags:
 *       - Examples
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/CreateExampleDto'
 *     responses:
 *       201:
 *         description: Example created successfully
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Example'
 *       400:
 *         description: Invalid input
 */
router.post('/', async (req: Request, res: Response) => {
  try {
    const { name, title, description, isActive } = req.body;

    if (!name || !title) {
      return res.status(400).json({ message: 'Name and title are required' });
    }

    const example = await prisma.example.create({
      data: {
        name,
        title,
        description: description || null,
        isActive: isActive !== undefined ? isActive : true,
      },
    });

    res.status(201).json(example);
  } catch (error) {
    res.status(400).json({ message: 'Error creating example', error: String(error) });
  }
});

/**
 * @swagger
 * /api/examples/{id}:
 *   put:
 *     summary: Update an example
 *     description: Updates an existing example record
 *     tags:
 *       - Examples
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *         description: The example ID
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/UpdateExampleDto'
 *     responses:
 *       200:
 *         description: Example updated successfully
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Example'
 *       404:
 *         description: Example not found
 *       400:
 *         description: Invalid input
 */
router.put('/:id', async (req: Request, res: Response) => {
  try {
    const id = parseInt(req.params.id);
    const { name, title, description, isActive } = req.body;

    // Check if example exists
    const existingExample = await prisma.example.findUnique({
      where: { id },
    });

    if (!existingExample) {
      return res.status(404).json({ message: `Example with ID ${id} not found` });
    }

    // Build update data object with only provided fields
    const updateData: any = {};
    if (name !== undefined) updateData.name = name;
    if (title !== undefined) updateData.title = title;
    if (description !== undefined) updateData.description = description;
    if (isActive !== undefined) updateData.isActive = isActive;

    const example = await prisma.example.update({
      where: { id },
      data: updateData,
    });

    res.json(example);
  } catch (error) {
    res.status(400).json({ message: 'Error updating example', error: String(error) });
  }
});

/**
 * @swagger
 * /api/examples/{id}:
 *   delete:
 *     summary: Delete an example
 *     description: Deletes an example record
 *     tags:
 *       - Examples
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *         description: The example ID
 *     responses:
 *       204:
 *         description: Example deleted successfully
 *       404:
 *         description: Example not found
 */
router.delete('/:id', async (req: Request, res: Response) => {
  try {
    const id = parseInt(req.params.id);

    // Check if example exists
    const existingExample = await prisma.example.findUnique({
      where: { id },
    });

    if (!existingExample) {
      return res.status(404).json({ message: `Example with ID ${id} not found` });
    }

    await prisma.example.delete({
      where: { id },
    });

    res.status(204).send();
  } catch (error) {
    res.status(500).json({ message: 'Error deleting example', error: String(error) });
  }
});

export default router;

